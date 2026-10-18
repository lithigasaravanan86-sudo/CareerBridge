import functools
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.init_db import get_db_connection

auth_bp = Blueprint('auth', __name__)

def login_required(view):
    """View decorator to protect student routes."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this feature.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    """View decorator to restrict routes to platform administrators."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('Administrative login required.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        if not session.get('is_admin'):
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('dashboard.index'))
        return view(**kwargs)
    return wrapped_view

@auth_bp.route('/')
def landing():
    """Landing Page & Public UI."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Aggregate stats for landing page metrics banner
    cursor.execute("SELECT COUNT(*) FROM job_roles")
    total_roles = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM standard_skills")
    total_skills = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 0")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM job_roles ORDER BY id ASC LIMIT 6")
    featured_roles = cursor.fetchall()

    conn.close()
    return render_template('index.html',
                           total_roles=total_roles,
                           total_skills=total_skills,
                           total_students=total_students,
                           featured_roles=featured_roles)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('is_admin'):
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please enter both email and password.', 'warning')
            return render_template('login.html', email=email)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['full_name'] = user['full_name']
            session['email'] = user['email']
            session['is_admin'] = bool(user['is_admin'])
            session.permanent = True

            flash(f"Welcome back, {user['full_name']}!", 'success')
            next_page = request.args.get('next')

            if user['is_admin']:
                return redirect(next_page or url_for('admin.dashboard'))
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        college_name = request.form.get('college_name', '').strip()
        degree = request.form.get('degree', '').strip()
        department = request.form.get('department', '').strip()
        grad_year_val = request.form.get('graduation_year', '').strip()
        career_goal = request.form.get('career_goal', '').strip()

        # Validation
        if not full_name or not email or not password:
            flash('Full Name, Email, and Password are required fields.', 'warning')
            return render_template('register.html', form_data=request.form)

        if password != confirm_password:
            flash('Passwords do not match. Please verify.', 'danger')
            return render_template('register.html', form_data=request.form)

        if len(password) < 6:
            flash('Password should be at least 6 characters long.', 'warning')
            return render_template('register.html', form_data=request.form)

        graduation_year = int(grad_year_val) if grad_year_val.isdigit() else 2026

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check duplicate email
        cursor.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            flash('An account with this email address already exists. Please sign in.', 'danger')
            return render_template('register.html', form_data=request.form)

        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users (full_name, email, password_hash, college_name, degree, department, graduation_year, career_goal, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            full_name, email, hashed_password, college_name, degree, department, graduation_year, career_goal
        ))
        conn.commit()
        new_user_id = cursor.lastrowid
        conn.close()

        # Automatically log the student in
        session.clear()
        session['user_id'] = new_user_id
        session['full_name'] = full_name
        session['email'] = email
        session['is_admin'] = False
        session.permanent = True

        flash('Registration successful! Welcome to CareerBridge. Start by adding your skills or uploading your resume.', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('register.html', form_data={})

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        college_name = request.form.get('college_name', '').strip()
        degree = request.form.get('degree', '').strip()
        department = request.form.get('department', '').strip()
        grad_year_val = request.form.get('graduation_year', '').strip()
        career_goal = request.form.get('career_goal', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not full_name:
            flash('Full Name is required.', 'warning')
        else:
            grad_year = int(grad_year_val) if grad_year_val.isdigit() else None

            if new_password:
                if new_password != confirm_password:
                    flash('New passwords do not match.', 'danger')
                    conn.close()
                    return redirect(url_for('auth.profile'))
                if len(new_password) < 6:
                    flash('New password must be at least 6 characters.', 'warning')
                    conn.close()
                    return redirect(url_for('auth.profile'))
                
                hashed_pass = generate_password_hash(new_password)
                cursor.execute("""
                    UPDATE users 
                    SET full_name = ?, college_name = ?, degree = ?, department = ?, 
                        graduation_year = ?, career_goal = ?, password_hash = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (full_name, college_name, degree, department, grad_year, career_goal, hashed_pass, user_id))
            else:
                cursor.execute("""
                    UPDATE users 
                    SET full_name = ?, college_name = ?, degree = ?, department = ?, 
                        graduation_year = ?, career_goal = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (full_name, college_name, degree, department, grad_year, career_goal, user_id))

            conn.commit()
            session['full_name'] = full_name
            flash('Profile updated successfully!', 'success')

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    # Calculate profile completion breakdown
    fields_to_check = [
        user['full_name'], user['email'], user['college_name'],
        user['degree'], user['department'], user['graduation_year'], user['career_goal']
    ]
    completed_fields = sum(1 for f in fields_to_check if f)
    profile_pct = round((completed_fields / len(fields_to_check)) * 100)

    # Check user skill count
    cursor.execute("SELECT COUNT(*) FROM user_skills WHERE user_id = ?", (user_id,))
    skill_count = cursor.fetchone()[0]

    conn.close()
    return render_template('profile.html', user=user, profile_pct=profile_pct, skill_count=skill_count)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('auth.login'))
