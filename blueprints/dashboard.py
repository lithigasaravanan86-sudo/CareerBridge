import json
from flask import Blueprint, render_template, session
from blueprints.auth import login_required
from database.init_db import get_db_connection
from services.matching_service import get_all_job_matches_for_user
from services.roadmap_service import get_user_all_roadmaps

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Fetch User Data
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    # 2. Fetch User Skills
    cursor.execute("""
        SELECT skill_name, category, proficiency 
        FROM user_skills 
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    user_skills = cursor.fetchall()
    total_skills = len(user_skills)

    # 3. Compute Category Distribution for Chart.js
    category_counts = {}
    for sk in user_skills:
        cat = sk['category'] or 'General'
        category_counts[cat] = category_counts.get(cat, 0) + 1

    chart_categories = list(category_counts.keys())
    chart_category_data = list(category_counts.values())

    # 4. Job Match Calculations
    job_matches = get_all_job_matches_for_user(user_id, conn)
    recommended_roles = [m for m in job_matches if m['match']['required_match_pct'] > 0]
    recommended_roles_count = len(recommended_roles)

    if job_matches:
        avg_job_match = round(sum(m['match']['required_match_pct'] for m in job_matches) / len(job_matches), 1)
    else:
        avg_job_match = 0.0

    # Top 6 roles for Chart.js Comparison Chart
    top_matches = job_matches[:6]
    chart_job_labels = [m['job']['title'] for m in top_matches]
    chart_job_required_pct = [m['match']['required_match_pct'] for m in top_matches]
    chart_job_overall_pct = [m['match']['overall_match_pct'] for m in top_matches]

    # 5. Roadmap Metrics
    roadmaps = get_user_all_roadmaps(user_id, conn)
    total_roadmap_items = 0
    completed_roadmap_items = 0

    for r in roadmaps:
        total_roadmap_items += (r['total_items'] or 0)
        completed_roadmap_items += (r['completed_items'] or 0)

    if total_roadmap_items > 0:
        overall_roadmap_progress = round((completed_roadmap_items / total_roadmap_items) * 100, 1)
    else:
        overall_roadmap_progress = 0.0

    # 6. Profile Completion Percentage
    profile_factors = [
        bool(user['full_name']),
        bool(user['email']),
        bool(user['college_name']),
        bool(user['degree']),
        bool(user['department']),
        bool(user['graduation_year']),
        bool(user['career_goal']),
        total_skills > 0,
        len(roadmaps) > 0
    ]
    profile_completion_pct = round((sum(1 for f in profile_factors if f) / len(profile_factors)) * 100)

    # 7. Next Up Milestones (Pending Roadmap Items)
    cursor.execute("""
        SELECT i.*, r.title as roadmap_title, j.title as job_title
        FROM roadmap_items i
        JOIN user_roadmaps r ON i.roadmap_id = r.id
        JOIN job_roles j ON r.job_id = j.id
        WHERE r.user_id = ? AND i.status != 'Completed'
        ORDER BY i.status DESC, i.order_index ASC
        LIMIT 4
    """, (user_id,))
    pending_milestones = cursor.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        user=user,
        total_skills=total_skills,
        recommended_roles_count=recommended_roles_count,
        avg_job_match=avg_job_match,
        overall_roadmap_progress=overall_roadmap_progress,
        profile_completion_pct=profile_completion_pct,
        top_matches=top_matches,
        recent_skills=user_skills[:6],
        roadmaps=roadmaps[:3],
        pending_milestones=pending_milestones,
        # JSON strings for Chart.js
        chart_categories_json=json.dumps(chart_categories),
        chart_category_data_json=json.dumps(chart_category_data),
        chart_job_labels_json=json.dumps(chart_job_labels),
        chart_job_required_pct_json=json.dumps(chart_job_required_pct),
        chart_job_overall_pct_json=json.dumps(chart_job_overall_pct)
    )
