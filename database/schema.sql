-- CareerBridge SQLite Schema

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    college_name TEXT,
    degree TEXT,
    department TEXT,
    graduation_year INTEGER,
    career_goal TEXT,
    is_admin INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS standard_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    aliases TEXT
);

CREATE TABLE IF NOT EXISTS user_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skill_name TEXT NOT NULL,
    category TEXT NOT NULL,
    proficiency TEXT NOT NULL CHECK(proficiency IN ('Beginner', 'Intermediate', 'Advanced')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, skill_name)
);

CREATE TABLE IF NOT EXISTS job_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    experience_level TEXT DEFAULT 'Entry to Mid Level',
    salary_range TEXT,
    learning_overview TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS job_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    skill_name TEXT NOT NULL,
    is_required INTEGER DEFAULT 1,
    minimum_proficiency TEXT DEFAULT 'Intermediate',
    importance_score REAL DEFAULT 1.0,
    FOREIGN KEY (job_id) REFERENCES job_roles(id) ON DELETE CASCADE,
    UNIQUE(job_id, skill_name)
);

CREATE TABLE IF NOT EXISTS user_roadmaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'In Progress',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_roles(id) ON DELETE CASCADE,
    UNIQUE(user_id, job_id)
);

CREATE TABLE IF NOT EXISTS roadmap_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roadmap_id INTEGER NOT NULL,
    skill_name TEXT NOT NULL,
    milestone_title TEXT NOT NULL,
    description TEXT NOT NULL,
    resource_title TEXT,
    resource_url TEXT,
    estimated_hours INTEGER DEFAULT 10,
    status TEXT DEFAULT 'Not Started' CHECK(status IN ('Not Started', 'In Progress', 'Completed')),
    order_index INTEGER DEFAULT 0,
    completed_at TIMESTAMP,
    FOREIGN KEY (roadmap_id) REFERENCES user_roadmaps(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS resume_uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    extracted_skills_json TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_user_skills_user ON user_skills(user_id);
CREATE INDEX IF NOT EXISTS idx_job_skills_job ON job_skills(job_id);
CREATE INDEX IF NOT EXISTS idx_user_roadmaps_user ON user_roadmaps(user_id);
CREATE INDEX IF NOT EXISTS idx_roadmap_items_roadmap ON roadmap_items(roadmap_id);
