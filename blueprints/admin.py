from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from blueprints.auth import admin_required
from database.init_db import get_db_connection
from config import Config

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Aggregate metrics
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 0")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM job_roles")
    total_roles = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM standard_skills")
    total_skills = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM user_roadmaps")
    total_roadmaps = cursor.fetchone()[0]

    # Fetch Job Roles with their associated skill counts
    cursor.execute("""
        SELECT j.*, 
               (SELECT COUNT(*) FROM job_skills WHERE job_id = j.id AND is_required = 1) as required_skills_count,
               (SELECT COUNT(*) FROM job_skills WHERE job_id = j.id AND is_required = 0) as preferred_skills_count
        FROM job_roles j
        ORDER BY j.id DESC
    """)
    job_roles = cursor.fetchall()

    # Fetch recent student registrations
    cursor.execute("""
        SELECT u.*, 
               (SELECT COUNT(*) FROM user_skills WHERE user_id = u.id) as skill_count,
               (SELECT COUNT(*) FROM user_roadmaps WHERE user_id = u.id) as roadmap_count
        FROM users u
        WHERE u.is_admin = 0
        ORDER BY u.created_at DESC
        LIMIT 10
    """)
    recent_students = cursor.fetchall()

    # Standard skills list
    cursor.execute("SELECT * FROM standard_skills ORDER BY category ASC, name ASC")
    all_standard_skills = cursor.fetchall()

    conn.close()

    return render_template(
        'admin_dashboard.html',
        total_students=total_students,
        total_roles=total_roles,
        total_skills=total_skills,
        total_roadmaps=total_roadmaps,
        job_roles=job_roles,
        recent_students=recent_students,
        all_standard_skills=all_standard_skills,
        categories=Config.SKILL_CATEGORIES
    )

@admin_bp.route('/jobs/add', methods=['POST'])
@admin_required
def add_job():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip()
    experience_level = request.form.get('experience_level', 'Entry to Mid Level').strip()
    salary_range = request.form.get('salary_range', '').strip()
    description = request.form.get('description', '').strip()
    learning_overview = request.form.get('learning_overview', '').strip()

    if not title or not category or not description:
        flash('Title, Category, and Description are required fields.', 'warning')
        return redirect(url_for('admin.dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO job_roles (title, category, description, experience_level, salary_range, learning_overview)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, category, description, experience_level, salary_range, learning_overview))
        conn.commit()
        flash(f"Job role '{title}' successfully added! You can now configure its required skills.", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"Error adding job role: {e}", 'danger')
    finally:
        conn.close()

    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/jobs/<int:job_id>/edit', methods=['POST'])
@admin_required
def edit_job(job_id):
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip()
    experience_level = request.form.get('experience_level', '').strip()
    salary_range = request.form.get('salary_range', '').strip()
    description = request.form.get('description', '').strip()
    learning_overview = request.form.get('learning_overview', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE job_roles 
            SET title = ?, category = ?, experience_level = ?, salary_range = ?, description = ?, learning_overview = ?
            WHERE id = ?
        """, (title, category, experience_level, salary_range, description, learning_overview, job_id))
        conn.commit()
        flash(f"Job role '{title}' updated successfully.", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"Failed to update job role: {e}", 'danger')
    finally:
        conn.close()

    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/jobs/<int:job_id>/delete', methods=['POST'])
@admin_required
def delete_job(job_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT title FROM job_roles WHERE id = ?", (job_id,))
    job = cursor.fetchone()

    if job:
        cursor.execute("DELETE FROM job_roles WHERE id = ?", (job_id,))
        conn.commit()
        flash(f"Job role '{job['title']}' deleted successfully.", 'info')
    else:
        flash('Job role not found.', 'warning')

    conn.close()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/jobs/<int:job_id>/skills/add', methods=['POST'])
@admin_required
def add_job_skill(job_id):
    skill_name = request.form.get('skill_name', '').strip()
    is_required = int(request.form.get('is_required', 1))
    min_prof = request.form.get('minimum_proficiency', 'Intermediate')

    if not skill_name:
        flash('Please select or specify a skill name.', 'warning')
        return redirect(url_for('admin.dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT OR REPLACE INTO job_skills (job_id, skill_name, is_required, minimum_proficiency, importance_score)
            VALUES (?, ?, ?, ?, ?)
        """, (job_id, skill_name, is_required, min_prof, 1.0 if is_required == 1 else 0.5))
        conn.commit()
        flash(f"Added '{skill_name}' to job role requirements.", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"Error associating skill: {e}", 'danger')
    finally:
        conn.close()

    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/jobs/<int:job_id>/skills/remove/<int:skill_id>', methods=['POST'])
@admin_required
def remove_job_skill(job_id, skill_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM job_skills WHERE id = ? AND job_id = ?", (skill_id, job_id))
    conn.commit()
    conn.close()

    flash('Skill requirement removed from job role.', 'info')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/standard-skills/add', methods=['POST'])
@admin_required
def add_standard_skill():
    name = request.form.get('name', '').strip()
    category = request.form.get('category', '').strip()
    aliases = request.form.get('aliases', '').strip()

    if not name or not category:
        flash('Skill Name and Category are required.', 'warning')
        return redirect(url_for('admin.dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO standard_skills (name, category, aliases)
            VALUES (?, ?, ?)
        """, (name, category, aliases))
        conn.commit()
        flash(f"Standard skill '{name}' added to dictionary.", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"Skill may already exist: {e}", 'warning')
    finally:
        conn.close()

    return redirect(url_for('admin.dashboard'))
