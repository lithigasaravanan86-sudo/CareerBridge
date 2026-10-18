from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from blueprints.auth import login_required
from database.init_db import get_db_connection
from config import Config

skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/skills', methods=['GET'])
@login_required
def index():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user skills
    cursor.execute("""
        SELECT * FROM user_skills 
        WHERE user_id = ?
        ORDER BY category ASC, skill_name ASC
    """, (user_id,))
    skills = cursor.fetchall()

    # Fetch standard skills list for autocomplete / dropdown
    cursor.execute("SELECT name, category FROM standard_skills ORDER BY name ASC")
    standard_skills = cursor.fetchall()

    # Category and proficiency counts
    prof_counts = {'Beginner': 0, 'Intermediate': 0, 'Advanced': 0}
    cat_counts = {}
    for s in skills:
        prof = s['proficiency']
        if prof in prof_counts:
            prof_counts[prof] += 1
        cat = s['category']
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    conn.close()

    return render_template(
        'skills.html',
        skills=skills,
        standard_skills=standard_skills,
        categories=Config.SKILL_CATEGORIES,
        proficiencies=Config.PROFICIENCY_LEVELS,
        prof_counts=prof_counts,
        cat_counts=cat_counts,
        total_skills=len(skills)
    )

@skills_bp.route('/skills/add', methods=['POST'])
@login_required
def add():
    user_id = session['user_id']
    skill_name = request.form.get('skill_name', '').strip()
    category = request.form.get('category', '').strip()
    proficiency = request.form.get('proficiency', '').strip()

    if not skill_name or not category or not proficiency:
        flash('Skill Name, Category, and Proficiency level are required.', 'warning')
        return redirect(url_for('skills.index'))

    if proficiency not in Config.PROFICIENCY_LEVELS:
        flash('Invalid proficiency level selected.', 'danger')
        return redirect(url_for('skills.index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check for duplicate
    cursor.execute("""
        SELECT id FROM user_skills 
        WHERE user_id = ? AND LOWER(skill_name) = LOWER(?)
    """, (user_id, skill_name))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        flash(f"'{skill_name}' is already in your skills profile. You can edit its proficiency instead.", 'info')
        return redirect(url_for('skills.index'))

    try:
        cursor.execute("""
            INSERT INTO user_skills (user_id, skill_name, category, proficiency)
            VALUES (?, ?, ?, ?)
        """, (user_id, skill_name, category, proficiency))
        conn.commit()
        flash(f"'{skill_name}' successfully added to your profile!", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"Error adding skill: {e}", 'danger')
    finally:
        conn.close()

    return redirect(url_for('skills.index'))

@skills_bp.route('/skills/edit/<int:skill_id>', methods=['POST'])
@login_required
def edit(skill_id):
    user_id = session['user_id']
    proficiency = request.form.get('proficiency', '').strip()
    category = request.form.get('category', '').strip()

    if proficiency not in Config.PROFICIENCY_LEVELS:
        flash('Invalid proficiency level.', 'danger')
        return redirect(url_for('skills.index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if category:
            cursor.execute("""
                UPDATE user_skills 
                SET proficiency = ?, category = ? 
                WHERE id = ? AND user_id = ?
            """, (proficiency, category, skill_id, user_id))
        else:
            cursor.execute("""
                UPDATE user_skills 
                SET proficiency = ? 
                WHERE id = ? AND user_id = ?
            """, (proficiency, skill_id, user_id))
        conn.commit()
        flash('Skill updated successfully.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Failed to update skill: {e}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('skills.index'))

@skills_bp.route('/skills/delete/<int:skill_id>', methods=['POST'])
@login_required
def delete(skill_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT skill_name FROM user_skills WHERE id = ? AND user_id = ?", (skill_id, user_id))
    skill = cursor.fetchone()

    if skill:
        cursor.execute("DELETE FROM user_skills WHERE id = ? AND user_id = ?", (skill_id, user_id))
        conn.commit()
        flash(f"Removed '{skill['skill_name']}' from your profile.", 'info')
    else:
        flash('Skill not found.', 'warning')

    conn.close()
    return redirect(url_for('skills.index'))
