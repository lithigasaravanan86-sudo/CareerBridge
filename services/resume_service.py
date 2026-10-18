import os
import re
from werkzeug.utils import secure_filename
from config import Config

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file using pdfplumber, PyMuPDF (fitz), with fallback to pypdf."""
    text = ""
    # 1. Try PyMuPDF (pymupdf) - extremely fast and accurate
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text += page_text + "\n"
        doc.close()
        if text.strip():
            return text
    except Exception as e:
        print(f"PyMuPDF extraction note: {e}, attempting pdfplumber...")

    # 2. Try pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except Exception as e:
        print(f"pdfplumber extraction note: {e}, falling back to pypdf...")

    # 3. Fallback to pypdf
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"pypdf extraction error: {e}")
        return text

def extract_text_from_docx(file_path):
    """Extracts text from a .docx file using python-docx."""
    text = ""
    try:
        import docx
        doc = docx.Document(file_path)
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text += paragraph.text + "\n"
        for table in doc.tables:
            for row in table.rows:
                row_text = " ".join([cell.text.strip() for cell in row.cells if cell.text.strip()])
                if row_text:
                    text += row_text + "\n"
        return text
    except Exception as e:
        print(f"docx extraction error: {e}")
        return text

def extract_resume_text(file_path):
    """Dispatches extraction based on file extension."""
    ext = os.path.splitext(file_path)[1].lower().replace('.', '')
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext == 'docx':
        return extract_text_from_docx(file_path)
    return ""

def build_skill_patterns(standard_skills):
    """
    Builds compiled regex patterns for standard skills and their aliases.
    Uses negative lookahead and lookbehind for alphanumeric characters to handle
    names with symbols like C++, C#, .NET, CI/CD, Node.js properly.
    """
    patterns = []
    for skill in standard_skills:
        skill_name = skill['name']
        category = skill['category']
        aliases_str = skill['aliases'] or ''
        terms = [skill_name]
        if aliases_str:
            terms.extend([a.strip() for a in aliases_str.split(',') if a.strip()])

        for term in terms:
            escaped_term = re.escape(term)
            pattern = re.compile(
                r'(?<![a-zA-Z0-9])' + escaped_term + r'(?![a-zA-Z0-9])',
                re.IGNORECASE
            )
            patterns.append({
                'skill_name': skill_name,
                'category': category,
                'term': term,
                'pattern': pattern
            })
    return patterns

def analyze_resume_text(text, user_id, conn):
    """
    Scans the extracted resume text against standard skills in the database.
    Checks existing user skills to flag already-added skills.
    Computes top matching job roles for preview.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name, category, aliases FROM standard_skills ORDER BY LENGTH(name) DESC")
    standard_skills = cursor.fetchall()

    patterns = build_skill_patterns(standard_skills)

    detected_dict = {}

    lower_text = text.lower()

    for item in patterns:
        matches = list(item['pattern'].finditer(text))
        if matches:
            count = len(matches)
            skill_name = item['skill_name']
            if skill_name not in detected_dict:
                detected_dict[skill_name] = {
                    'name': skill_name,
                    'category': item['category'],
                    'count': count,
                    'terms_matched': {item['term']}
                }
            else:
                detected_dict[skill_name]['count'] += count
                detected_dict[skill_name]['terms_matched'].add(item['term'])

    # Query current user skills to show which are already in profile
    cursor.execute("SELECT LOWER(skill_name) as sk_name FROM user_skills WHERE user_id = ?", (user_id,))
    existing_skills = {row['sk_name'] for row in cursor.fetchall()}

    detected_skills_list = []
    for sk_name, sk_info in detected_dict.items():
        is_existing = sk_name.lower() in existing_skills
        
        # Suggest proficiency based on frequency and context
        count = sk_info['count']
        if count >= 4:
            suggested_prof = 'Advanced'
        elif count >= 2:
            suggested_prof = 'Intermediate'
        else:
            suggested_prof = 'Intermediate'

        detected_skills_list.append({
            'name': sk_info['name'],
            'category': sk_info['category'],
            'count': count,
            'is_existing': is_existing,
            'suggested_proficiency': suggested_prof
        })

    # Sort: non-existing first, then by count descending
    detected_skills_list.sort(key=lambda x: (not x['is_existing'], x['count']), reverse=True)

    # Calculate preview role matches based on detected skills
    user_skills_map = {
        item['name'].lower(): {
            'original_name': item['name'],
            'category': item['category'],
            'proficiency': item['suggested_proficiency']
        }
        for item in detected_skills_list
    }

    from services.matching_service import calculate_job_match
    cursor.execute("SELECT id, title, category FROM job_roles")
    all_jobs = cursor.fetchall()

    recommended_roles = []
    for job in all_jobs:
        cursor.execute("""
            SELECT js.*, COALESCE(s.category, 'General') as category
            FROM job_skills js
            LEFT JOIN standard_skills s ON LOWER(js.skill_name) = LOWER(s.name)
            WHERE js.job_id = ?
        """, (job['id'],))
        job_skills = cursor.fetchall()
        match_res = calculate_job_match(user_skills_map, job_skills)
        if match_res['required_match_pct'] > 0:
            recommended_roles.append({
                'title': job['title'],
                'category': job['category'],
                'required_match_pct': match_res['required_match_pct'],
                'overall_match_pct': match_res['overall_match_pct']
            })

    recommended_roles.sort(key=lambda x: x['required_match_pct'], reverse=True)

    # Clean preview text
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    snippet = " ".join(lines[:10])
    if len(snippet) > 400:
        snippet = snippet[:400] + "..."

    return {
        'detected_skills': detected_skills_list,
        'total_detected': len(detected_skills_list),
        'new_skills_count': len([s for s in detected_skills_list if not s['is_existing']]),
        'recommended_roles': recommended_roles[:4],
        'text_snippet': snippet
    }
