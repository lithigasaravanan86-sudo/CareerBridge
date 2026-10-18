def calculate_job_match(user_skills_map, job_skills):
    """
    Calculates match percentage and skill gap for a specific job role.
    
    Rule-based matching formula:
    Required Match % = (Matched Required Skills / Total Required Skills) * 100
    Overall Match %  = Weighted score taking both required and preferred skills into account.

    user_skills_map: dict of { skill_name.lower(): { 'proficiency': str, 'category': str, 'original_name': str } }
    job_skills: list of dicts/rows containing skill_name, is_required, minimum_proficiency, category
    """
    total_required = 0
    matched_required = 0
    total_preferred = 0
    matched_preferred = 0

    matched_skills = []
    missing_skills = []

    proficiency_rank = {
        'Beginner': 1,
        'Intermediate': 2,
        'Advanced': 3
    }

    for skill in job_skills:
        skill_name = skill['skill_name']
        is_req = bool(skill['is_required'])
        min_prof = skill['minimum_proficiency'] or 'Intermediate'
        category = skill['category'] if 'category' in skill.keys() and skill['category'] else 'General'

        clean_key = skill_name.strip().lower()
        user_has_skill = clean_key in user_skills_map

        if is_req:
            total_required += 1
            if user_has_skill:
                matched_required += 1
        else:
            total_preferred += 1
            if user_has_skill:
                matched_preferred += 1

        if user_has_skill:
            user_prof = user_skills_map[clean_key]['proficiency']
            user_rank = proficiency_rank.get(user_prof, 1)
            target_rank = proficiency_rank.get(min_prof, 2)
            has_prof_gap = user_rank < target_rank

            matched_skills.append({
                'skill_name': skill_name,
                'category': user_skills_map[clean_key]['category'] or category,
                'is_required': is_req,
                'minimum_proficiency': min_prof,
                'user_proficiency': user_prof,
                'proficiency_gap': has_prof_gap
            })
        else:
            missing_skills.append({
                'skill_name': skill_name,
                'category': category,
                'is_required': is_req,
                'minimum_proficiency': min_prof
            })

    # Formula required by specification:
    if total_required > 0:
        required_match_pct = round((matched_required / total_required) * 100, 1)
    else:
        required_match_pct = 100.0 if len(job_skills) == 0 else 0.0

    # Composite overall score (80% required, 20% preferred)
    if total_preferred > 0:
        preferred_match_pct = round((matched_preferred / total_preferred) * 100, 1)
        overall_match_pct = round((required_match_pct * 0.8) + (preferred_match_pct * 0.2), 1)
    else:
        preferred_match_pct = 100.0
        overall_match_pct = required_match_pct

    return {
        'required_match_pct': required_match_pct,
        'preferred_match_pct': preferred_match_pct,
        'overall_match_pct': overall_match_pct,
        'matched_required': matched_required,
        'total_required': total_required,
        'matched_preferred': matched_preferred,
        'total_preferred': total_preferred,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'total_skills_count': len(job_skills),
        'matched_total_count': len(matched_skills),
        'missing_total_count': len(missing_skills)
    }

def get_user_skills_map(user_id, conn):
    """Fetches user skills into a lowercase lookup dictionary."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT skill_name, category, proficiency 
        FROM user_skills 
        WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    return {
        row['skill_name'].strip().lower(): {
            'original_name': row['skill_name'],
            'category': row['category'],
            'proficiency': row['proficiency']
        }
        for row in rows
    }

def get_all_job_matches_for_user(user_id, conn):
    """
    Computes matches for all available job roles for a student.
    Returns list of job roles with match percentages and metrics sorted descending by match.
    """
    user_skills_map = get_user_skills_map(user_id, conn)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM job_roles ORDER BY title ASC")
    jobs = cursor.fetchall()

    results = []
    for job in jobs:
        cursor.execute("""
            SELECT js.*, COALESCE(s.category, 'General') as category
            FROM job_skills js
            LEFT JOIN standard_skills s ON LOWER(js.skill_name) = LOWER(s.name)
            WHERE js.job_id = ?
            ORDER BY js.is_required DESC, js.skill_name ASC
        """, (job['id'],))
        job_skills = cursor.fetchall()

        match_data = calculate_job_match(user_skills_map, job_skills)

        # Check if user already generated a roadmap for this job
        cursor.execute("""
            SELECT id, status FROM user_roadmaps 
            WHERE user_id = ? AND job_id = ?
        """, (user_id, job['id']))
        roadmap_row = cursor.fetchone()

        results.append({
            'job': dict(job),
            'match': match_data,
            'has_roadmap': bool(roadmap_row),
            'roadmap_id': roadmap_row['id'] if roadmap_row else None
        })

    # Sort primarily by required_match_pct descending, then overall_match_pct descending
    results.sort(key=lambda x: (x['match']['required_match_pct'], x['match']['overall_match_pct']), reverse=True)
    return results

def get_skill_gap_for_job(user_id, job_id, conn):
    """
    Retrieves in-depth skill gap analysis for a specific job role and user.
    """
    user_skills_map = get_user_skills_map(user_id, conn)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM job_roles WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    if not job:
        return None

    cursor.execute("""
        SELECT js.*, COALESCE(s.category, 'General') as category
        FROM job_skills js
        LEFT JOIN standard_skills s ON LOWER(js.skill_name) = LOWER(s.name)
        WHERE js.job_id = ?
        ORDER BY js.is_required DESC, js.skill_name ASC
    """, (job_id,))
    job_skills = cursor.fetchall()

    match_data = calculate_job_match(user_skills_map, job_skills)

    # Check for active roadmap
    cursor.execute("""
        SELECT id, status FROM user_roadmaps 
        WHERE user_id = ? AND job_id = ?
    """, (user_id, job_id))
    roadmap_row = cursor.fetchone()

    return {
        'job': dict(job),
        'match': match_data,
        'has_roadmap': bool(roadmap_row),
        'roadmap_id': roadmap_row['id'] if roadmap_row else None,
        'user_total_skills': len(user_skills_map)
    }
