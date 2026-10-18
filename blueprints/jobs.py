from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from blueprints.auth import login_required
from database.init_db import get_db_connection
from services.matching_service import get_all_job_matches_for_user, get_skill_gap_for_job

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs')
@login_required
def index():
    user_id = session['user_id']
    conn = get_db_connection()

    all_matches = get_all_job_matches_for_user(user_id, conn)

    # Optional query filters
    search_query = request.args.get('q', '').strip().lower()
    category_filter = request.args.get('category', '').strip()
    min_match_val = request.args.get('min_match', '').strip()

    filtered_matches = all_matches

    if search_query:
        filtered_matches = [
            m for m in filtered_matches 
            if search_query in m['job']['title'].lower() 
            or search_query in m['job']['description'].lower()
            or search_query in m['job']['category'].lower()
        ]

    if category_filter:
        filtered_matches = [
            m for m in filtered_matches 
            if m['job']['category'].lower() == category_filter.lower()
        ]

    if min_match_val.isdigit():
        min_match_num = int(min_match_val)
        filtered_matches = [
            m for m in filtered_matches 
            if m['match']['required_match_pct'] >= min_match_num
        ]

    # Unique categories for filter dropdown
    categories = sorted(list({m['job']['category'] for m in all_matches}))

    conn.close()

    return render_template(
        'jobs.html',
        job_matches=filtered_matches,
        all_count=len(all_matches),
        filtered_count=len(filtered_matches),
        categories=categories,
        search_query=search_query,
        category_filter=category_filter,
        min_match_val=min_match_val
    )

@jobs_bp.route('/jobs/<int:job_id>')
@login_required
def detail(job_id):
    user_id = session['user_id']
    conn = get_db_connection()

    gap_data = get_skill_gap_for_job(user_id, job_id, conn)
    if not gap_data:
        conn.close()
        flash('Job role not found.', 'danger')
        return redirect(url_for('jobs.index'))

    conn.close()
    return render_template(
        'job_detail.html',
        job=gap_data['job'],
        match=gap_data['match'],
        has_roadmap=gap_data['has_roadmap'],
        roadmap_id=gap_data['roadmap_id']
    )

@jobs_bp.route('/jobs/<int:job_id>/skill-gap')
@login_required
def skill_gap(job_id):
    user_id = session['user_id']
    conn = get_db_connection()

    gap_data = get_skill_gap_for_job(user_id, job_id, conn)
    if not gap_data:
        conn.close()
        flash('Job role not found.', 'danger')
        return redirect(url_for('jobs.index'))

    conn.close()
    return render_template(
        'skill_gap.html',
        job=gap_data['job'],
        match=gap_data['match'],
        has_roadmap=gap_data['has_roadmap'],
        roadmap_id=gap_data['roadmap_id'],
        user_total_skills=gap_data['user_total_skills']
    )
