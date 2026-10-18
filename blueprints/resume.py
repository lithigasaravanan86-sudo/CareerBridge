import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from blueprints.auth import login_required
from database.init_db import get_db_connection
from config import Config
from services.resume_service import extract_resume_text, analyze_resume_text

resume_bp = Blueprint('resume', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@resume_bp.route('/resume-analyzer', methods=['GET', 'POST'])
@login_required
def index():
    user_id = session['user_id']

    if request.method == 'POST':
        if 'resume_file' not in request.files:
            flash('No file selected. Please choose a PDF or DOCX resume.', 'warning')
            return redirect(request.url)

        file = request.files['resume_file']
        if file.filename == '':
            flash('No file selected.', 'warning')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Unsupported file type. Please upload a .pdf or .docx document under 5MB.', 'danger')
            return redirect(request.url)

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > Config.MAX_CONTENT_LENGTH:
            flash('File size exceeds the 5MB limit. Please upload a smaller document.', 'danger')
            return redirect(request.url)

        # Save temporarily
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(file.filename)
        save_path = os.path.join(Config.UPLOAD_FOLDER, f"user_{user_id}_{filename}")
        file.save(save_path)

        try:
            # Parse text locally
            text = extract_resume_text(save_path)
            if not text or not text.strip():
                flash('Could not extract readable text from this document. Please ensure it is not an image-only scanned PDF.', 'warning')
                if os.path.exists(save_path):
                    os.remove(save_path)
                return redirect(request.url)

            conn = get_db_connection()
            analysis = analyze_resume_text(text, user_id, conn)

            # Record upload history in resume_uploads
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO resume_uploads (user_id, filename, extracted_skills_json)
                VALUES (?, ?, ?)
            """, (user_id, filename, json.dumps([s['name'] for s in analysis['detected_skills']])))
            conn.commit()
            conn.close()

            # Clean up uploaded file from disk after parsing
            if os.path.exists(save_path):
                os.remove(save_path)

            return render_template(
                'resume_analyzer.html',
                analysis=analysis,
                filename=filename,
                categories=Config.SKILL_CATEGORIES,
                proficiencies=Config.PROFICIENCY_LEVELS,
                step='review'
            )

        except Exception as e:
            if os.path.exists(save_path):
                os.remove(save_path)
            flash(f'An error occurred while analyzing the resume: {e}', 'danger')
            return redirect(request.url)

    # GET request - show upload form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT filename, uploaded_at, extracted_skills_json 
        FROM resume_uploads 
        WHERE user_id = ? 
        ORDER BY uploaded_at DESC 
        LIMIT 3
    """, (user_id,))
    recent_uploads = cursor.fetchall()
    conn.close()

    return render_template('resume_analyzer.html', recent_uploads=recent_uploads, step='upload')

@resume_bp.route('/resume-analyzer/confirm', methods=['POST'])
@login_required
def confirm_skills():
    user_id = session['user_id']
    selected_skills = request.form.getlist('selected_skills')

    if not selected_skills:
        flash('No skills were selected to add.', 'warning')
        return redirect(url_for('resume.index'))

    conn = get_db_connection()
    cursor = conn.cursor()
    added_count = 0
    updated_count = 0

    for skill_name in selected_skills:
        category = request.form.get(f'cat_{skill_name}', 'Tools')
        proficiency = request.form.get(f'prof_{skill_name}', 'Intermediate')

        if proficiency not in Config.PROFICIENCY_LEVELS:
            proficiency = 'Intermediate'

        # Check if skill exists
        cursor.execute("SELECT id FROM user_skills WHERE user_id = ? AND LOWER(skill_name) = LOWER(?)", (user_id, skill_name))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE user_skills 
                SET proficiency = ?, category = ? 
                WHERE id = ?
            """, (proficiency, category, existing['id']))
            updated_count += 1
        else:
            cursor.execute("""
                INSERT INTO user_skills (user_id, skill_name, category, proficiency)
                VALUES (?, ?, ?, ?)
            """, (user_id, skill_name, category, proficiency))
            added_count += 1

    conn.commit()
    conn.close()

    flash(f'Successfully imported {added_count} new skills and updated {updated_count} existing skills to your profile!', 'success')
    return redirect(url_for('skills.index'))
