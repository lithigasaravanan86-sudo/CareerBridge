import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'careerbridge-super-secret-key-2026-production')
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'careerbridge.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB limit
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}

    SKILL_CATEGORIES = [
        'Languages',
        'Web Dev',
        'Databases',
        'Data Analytics',
        'Cloud',
        'Cybersecurity',
        'Tools',
        'Soft Skills'
    ]

    PROFICIENCY_LEVELS = ['Beginner', 'Intermediate', 'Advanced']

    DEFAULT_ADMIN_EMAIL = 'admin@careerbridge.com'
    DEFAULT_ADMIN_PASSWORD = 'Admin@123'
