import sqlite3
from werkzeug.security import generate_password_hash

def seed_database(conn):
    cursor = conn.cursor()

    # 1. Seed Default Admin
    cursor.execute("SELECT id FROM users WHERE email = ?", ('admin@careerbridge.com',))
    if not cursor.fetchone():
        admin_pass_hash = generate_password_hash('Admin@123')
        cursor.execute("""
            INSERT INTO users (full_name, email, password_hash, college_name, degree, department, graduation_year, career_goal, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'System Administrator',
            'admin@careerbridge.com',
            admin_pass_hash,
            'CareerBridge HQ',
            'B.Tech / M.Tech',
            'Platform Administration',
            2024,
            'Empowering students with career navigation and skill readiness',
            1
        ))

    # 2. Seed Standard Skills Dictionary
    skills = [
        # Languages
        ('Python', 'Languages', 'python3, py, python 3'),
        ('JavaScript', 'Languages', 'js, es6, ecmascript, vanillajs'),
        ('TypeScript', 'Languages', 'ts, typescript'),
        ('Java', 'Languages', 'java, core java, j2ee'),
        ('C++', 'Languages', 'cpp, c plus plus'),
        ('C#', 'Languages', 'csharp, c-sharp, .net c#'),
        ('Go', 'Languages', 'golang, go lang'),
        ('Rust', 'Languages', 'rustlang'),
        ('PHP', 'Languages', 'php7, php8'),
        ('SQL', 'Languages', 'structured query language, t-sql, pl/sql'),
        ('HTML', 'Languages', 'html5, semantic html'),
        ('CSS', 'Languages', 'css3, styling, stylesheets'),
        ('Bash', 'Languages', 'shell scripting, sh, zsh'),

        # Web Dev
        ('React', 'Web Dev', 'react.js, reactjs'),
        ('Next.js', 'Web Dev', 'nextjs, next.js 14'),
        ('Node.js', 'Web Dev', 'nodejs, node'),
        ('Express.js', 'Web Dev', 'express, expressjs'),
        ('Flask', 'Web Dev', 'flask microframework, python flask'),
        ('Django', 'Web Dev', 'django framework, python django'),
        ('FastAPI', 'Web Dev', 'fastapi, python fastapi'),
        ('Vue.js', 'Web Dev', 'vue, vuejs, vue3'),
        ('Angular', 'Web Dev', 'angularjs, angular 2+'),
        ('REST APIs', 'Web Dev', 'restful api, rest service, api design'),
        ('GraphQL', 'Web Dev', 'graphql api, apollo client'),
        ('Tailwind CSS', 'Web Dev', 'tailwind, tailwindcss'),
        ('Bootstrap', 'Web Dev', 'bootstrap 5, bootstrap4'),
        ('Spring Boot', 'Web Dev', 'springboot, spring framework'),
        ('Microservices', 'Web Dev', 'microservice architecture, distributed systems'),

        # Databases
        ('PostgreSQL', 'Databases', 'postgres, psql'),
        ('MySQL', 'Databases', 'mariadb, mysql 8'),
        ('SQLite', 'Databases', 'sqlite3, embedded database'),
        ('MongoDB', 'Databases', 'mongo, nosql mongodb'),
        ('Redis', 'Databases', 'redis cache, in-memory store'),
        ('Firebase', 'Databases', 'firestore, firebase real-time database'),
        ('Oracle DB', 'Databases', 'oracle database, plsql'),
        ('DynamoDB', 'Databases', 'aws dynamodb, nosql table'),

        # Data Analytics
        ('Pandas', 'Data Analytics', 'pandas library, dataframe manipulation'),
        ('NumPy', 'Data Analytics', 'numpy array, numerical python'),
        ('Tableau', 'Data Analytics', 'tableau desktop, data dashboards'),
        ('Power BI', 'Data Analytics', 'powerbi, microsoft power bi'),
        ('Excel', 'Data Analytics', 'ms excel, advanced excel, vlookup, pivot tables'),
        ('Data Visualization', 'Data Analytics', 'charts, dashboards, bi visualization'),
        ('Matplotlib', 'Data Analytics', 'matplotlib plotting'),
        ('Seaborn', 'Data Analytics', 'seaborn data graphics'),
        ('Statistics', 'Data Analytics', 'statistical analysis, hypothesis testing, probability'),
        ('SQL Analytics', 'Data Analytics', 'window functions, cte, aggregations'),
        ('Machine Learning', 'Data Analytics', 'scikit-learn, ml algorithms, supervised learning'),
        ('Data Preprocessing', 'Data Analytics', 'feature engineering, cleaning, etl'),

        # Cloud
        ('AWS', 'Cloud', 'amazon web services, ec2, s3, lambda'),
        ('Microsoft Azure', 'Cloud', 'azure cloud, azure devops'),
        ('Google Cloud', 'Cloud', 'gcp, google cloud platform'),
        ('Docker', 'Cloud', 'containerization, dockerfile, docker-compose'),
        ('Kubernetes', 'Cloud', 'k8s, container orchestration'),
        ('CI/CD', 'Cloud', 'continuous integration, continuous deployment, github actions'),
        ('Terraform', 'Cloud', 'infrastructure as code, iac'),
        ('Linux', 'Cloud', 'ubuntu, centos, debian, red hat, linux cli'),
        ('Prometheus', 'Cloud', 'monitoring, grafana, metrics'),

        # Cybersecurity
        ('Network Security', 'Cybersecurity', 'tcp/ip, firewalls, routing, vpn'),
        ('Penetration Testing', 'Cybersecurity', 'pen testing, ethical hacking, kali linux'),
        ('Ethical Hacking', 'Cybersecurity', 'white hat, exploit analysis'),
        ('OWASP Top 10', 'Cybersecurity', 'web application security, xss, sql injection, csrf'),
        ('Cryptography', 'Cybersecurity', 'encryption, ssl, tls, rsa, hashing'),
        ('Wireshark', 'Cybersecurity', 'packet capture, network analysis'),
        ('SIEM', 'Cybersecurity', 'splunk, qradar, security monitoring'),
        ('Incident Response', 'Cybersecurity', 'forensics, threat mitigation, security alerts'),

        # Tools
        ('Git', 'Tools', 'version control, git cli, branching'),
        ('GitHub', 'Tools', 'gitlab, bitbucket, pull requests'),
        ('Postman', 'Tools', 'api testing, postman collections'),
        ('VS Code', 'Tools', 'visual studio code, ide configuration'),
        ('Jira', 'Tools', 'agile ticketing, sprint tracking, scrum board'),
        ('Jenkins', 'Tools', 'automation server, build pipelines'),
        ('PyTest', 'Tools', 'unit testing, pytest fixtures, tdd'),
        ('Figma', 'Tools', 'ui prototyping, wireframing, design mockup'),

        # Soft Skills
        ('Problem Solving', 'Soft Skills', 'analytical skills, debugging mindset, algorithmic thinking'),
        ('Communication', 'Soft Skills', 'verbal communication, written reports, presentation'),
        ('Team Collaboration', 'Soft Skills', 'pair programming, cross-functional teamwork'),
        ('Time Management', 'Soft Skills', 'prioritization, deadline adherence, planning'),
        ('Agile/Scrum', 'Soft Skills', 'standups, retrospectives, user stories'),
        ('Critical Thinking', 'Soft Skills', 'requirement evaluation, architectural reasoning')
    ]

    for name, cat, aliases in skills:
        cursor.execute("""
            INSERT OR IGNORE INTO standard_skills (name, category, aliases)
            VALUES (?, ?, ?)
        """, (name, cat, aliases))

    # 3. Seed Realistic Job Roles & Requirements (12 Roles)
    roles = [
        {
            'title': 'Python Developer',
            'category': 'Backend & Scripting',
            'description': 'Design, build, and deploy high-performance backend systems, automation scripts, and API services using Python and contemporary frameworks.',
            'experience_level': 'Entry to Mid Level',
            'salary_range': '$70,000 - $110,000 / year',
            'learning_overview': 'Master core Python mechanics, object-oriented patterns, database querying via SQL/ORM, RESTful API development, and unit testing.',
            'skills': [
                ('Python', 1, 'Advanced'),
                ('SQL', 1, 'Intermediate'),
                ('Flask', 1, 'Intermediate'),
                ('Git', 1, 'Intermediate'),
                ('REST APIs', 1, 'Intermediate'),
                ('PostgreSQL', 0, 'Intermediate'),
                ('Docker', 0, 'Beginner'),
                ('PyTest', 0, 'Intermediate'),
                ('Linux', 0, 'Beginner'),
                ('Problem Solving', 0, 'Intermediate')
            ]
        },
        {
            'title': 'Full-Stack Web Developer',
            'category': 'Web Development',
            'description': 'Engineer interactive front-end web applications seamlessly integrated with resilient back-end architectures, databases, and third-party APIs.',
            'experience_level': 'Entry to Mid Level',
            'salary_range': '$75,000 - $120,000 / year',
            'learning_overview': 'Build end-to-end web applications combining modern frontend frameworks, server-side APIs, database modeling, and deployment strategies.',
            'skills': [
                ('HTML', 1, 'Advanced'),
                ('CSS', 1, 'Advanced'),
                ('JavaScript', 1, 'Advanced'),
                ('React', 1, 'Intermediate'),
                ('Node.js', 1, 'Intermediate'),
                ('REST APIs', 1, 'Intermediate'),
                ('SQL', 1, 'Intermediate'),
                ('Git', 1, 'Intermediate'),
                ('TypeScript', 0, 'Intermediate'),
                ('MongoDB', 0, 'Beginner'),
                ('Docker', 0, 'Beginner'),
                ('Tailwind CSS', 0, 'Intermediate')
            ]
        },
        {
            'title': 'Data Analyst',
            'category': 'Data & Analytics',
            'description': 'Extract insights from complex data sets, curate executive dashboards, and drive business decision-making through data modeling and visualization.',
            'experience_level': 'Entry Level',
            'salary_range': '$65,000 - $95,000 / year',
            'learning_overview': 'Develop proficiency in SQL querying, Python analytics with Pandas, spreadsheet modeling, and storytelling through Tableau or Power BI.',
            'skills': [
                ('SQL', 1, 'Advanced'),
                ('Python', 1, 'Intermediate'),
                ('Pandas', 1, 'Intermediate'),
                ('Excel', 1, 'Advanced'),
                ('Tableau', 1, 'Intermediate'),
                ('Data Visualization', 1, 'Intermediate'),
                ('Power BI', 0, 'Intermediate'),
                ('NumPy', 0, 'Intermediate'),
                ('Statistics', 0, 'Intermediate'),
                ('Communication', 0, 'Intermediate')
            ]
        },
        {
            'title': 'Data Engineer',
            'category': 'Data Engineering',
            'description': 'Construct robust data pipelines, ETL workflows, and scalable distributed storage architectures to support enterprise analytical applications.',
            'experience_level': 'Mid Level',
            'salary_range': '$90,000 - $140,000 / year',
            'learning_overview': 'Master SQL optimizations, Python ETL pipelines, PostgreSQL database tuning, containerization with Docker, and cloud streaming tools.',
            'skills': [
                ('Python', 1, 'Advanced'),
                ('SQL', 1, 'Advanced'),
                ('PostgreSQL', 1, 'Intermediate'),
                ('Docker', 1, 'Intermediate'),
                ('Linux', 1, 'Intermediate'),
                ('Git', 1, 'Intermediate'),
                ('AWS', 0, 'Intermediate'),
                ('Redis', 0, 'Beginner'),
                ('CI/CD', 0, 'Beginner'),
                ('Pandas', 0, 'Intermediate')
            ]
        },
        {
            'title': 'Frontend Developer',
            'category': 'Web Development',
            'description': 'Craft visually captivating, accessible, and high-performance user interfaces and single-page applications using modern JavaScript and React.',
            'experience_level': 'Entry to Mid Level',
            'salary_range': '$70,000 - $110,000 / year',
            'learning_overview': 'Focus on CSS layouts, JavaScript ES6+, state management in React, responsive design systems, and component architecture.',
            'skills': [
                ('HTML', 1, 'Advanced'),
                ('CSS', 1, 'Advanced'),
                ('JavaScript', 1, 'Advanced'),
                ('React', 1, 'Intermediate'),
                ('Git', 1, 'Intermediate'),
                ('Bootstrap', 1, 'Intermediate'),
                ('TypeScript', 0, 'Intermediate'),
                ('Next.js', 0, 'Beginner'),
                ('Tailwind CSS', 0, 'Intermediate'),
                ('Figma', 0, 'Beginner')
            ]
        },
        {
            'title': 'Backend Engineer',
            'category': 'Backend & Cloud',
            'description': 'Architect fault-tolerant microservices, maintain relational and NoSQL databases, and implement scalable API endpoints handling mission-critical traffic.',
            'experience_level': 'Mid Level',
            'salary_range': '$85,000 - $135,000 / year',
            'learning_overview': 'Deep dive into RESTful services, database indexing and transactions, caching strategies with Redis, container orchestration, and authentication protocols.',
            'skills': [
                ('Python', 1, 'Advanced'),
                ('REST APIs', 1, 'Advanced'),
                ('SQL', 1, 'Advanced'),
                ('PostgreSQL', 1, 'Intermediate'),
                ('Docker', 1, 'Intermediate'),
                ('Git', 1, 'Intermediate'),
                ('Linux', 1, 'Intermediate'),
                ('Redis', 0, 'Intermediate'),
                ('CI/CD', 0, 'Intermediate'),
                ('AWS', 0, 'Beginner')
            ]
        },
        {
            'title': 'Cybersecurity Analyst',
            'category': 'Security',
            'description': 'Safeguard organization networks, conduct vulnerability assessments, monitor security incidents, and maintain security hygiene against modern threats.',
            'experience_level': 'Entry to Mid Level',
            'salary_range': '$75,000 - $115,000 / year',
            'learning_overview': 'Understand network protocols, packet inspection with Wireshark, application vulnerability discovery via OWASP Top 10, and Linux security auditing.',
            'skills': [
                ('Network Security', 1, 'Intermediate'),
                ('Linux', 1, 'Intermediate'),
                ('Wireshark', 1, 'Intermediate'),
                ('OWASP Top 10', 1, 'Intermediate'),
                ('Cryptography', 1, 'Intermediate'),
                ('Python', 1, 'Beginner'),
                ('Penetration Testing', 0, 'Beginner'),
                ('Ethical Hacking', 0, 'Beginner'),
                ('Incident Response', 0, 'Beginner'),
                ('Problem Solving', 0, 'Intermediate')
            ]
        },
        {
            'title': 'Cloud & DevOps Engineer',
            'category': 'Cloud & Infrastructure',
            'description': 'Automate infrastructure deployment, orchestrate scalable containers, manage continuous delivery pipelines, and ensure 99.99% system availability.',
            'experience_level': 'Mid Level',
            'salary_range': '$95,000 - $145,000 / year',
            'learning_overview': 'Learn cloud foundations in AWS, Docker containerization, Kubernetes cluster management, CI/CD with GitHub Actions/Jenkins, and Linux administration.',
            'skills': [
                ('Linux', 1, 'Advanced'),
                ('Docker', 1, 'Advanced'),
                ('AWS', 1, 'Intermediate'),
                ('CI/CD', 1, 'Intermediate'),
                ('Git', 1, 'Intermediate'),
                ('Kubernetes', 1, 'Beginner'),
                ('Terraform', 0, 'Beginner'),
                ('Python', 0, 'Intermediate'),
                ('Bash', 0, 'Intermediate'),
                ('Prometheus', 0, 'Beginner')
            ]
        },
        {
            'title': 'Machine Learning Engineer',
            'category': 'Artificial Intelligence',
            'description': 'Build, optimize, and deploy machine learning models and predictive pipelines that solve complex classification, regression, and ranking problems.',
            'experience_level': 'Mid Level',
            'salary_range': '$95,000 - $150,000 / year',
            'learning_overview': 'Master mathematical statistics, exploratory data analysis with Pandas and NumPy, supervised and unsupervised ML, model validation, and API deployment.',
            'skills': [
                ('Python', 1, 'Advanced'),
                ('NumPy', 1, 'Advanced'),
                ('Pandas', 1, 'Advanced'),
                ('Machine Learning', 1, 'Intermediate'),
                ('Data Preprocessing', 1, 'Intermediate'),
                ('Git', 1, 'Intermediate'),
                ('SQL', 1, 'Intermediate'),
                ('Flask', 0, 'Intermediate'),
                ('Docker', 0, 'Beginner'),
                ('Data Visualization', 0, 'Intermediate')
            ]
        },
        {
            'title': 'Mobile App Developer',
            'category': 'Mobile Development',
            'description': 'Develop fluid, responsive, and intuitive cross-platform mobile experiences for iOS and Android devices with robust offline support and REST API sync.',
            'experience_level': 'Entry to Mid Level',
            'salary_range': '$70,000 - $115,000 / year',
            'learning_overview': 'Master UI component composition, state management, mobile API networking, client-side caching with SQLite, and app store deployment practices.',
            'skills': [
                ('JavaScript', 1, 'Advanced'),
                ('React', 1, 'Intermediate'),
                ('REST APIs', 1, 'Intermediate'),
                ('Git', 1, 'Intermediate'),
                ('HTML', 1, 'Intermediate'),
                ('CSS', 1, 'Intermediate'),
                ('TypeScript', 0, 'Intermediate'),
                ('Firebase', 0, 'Intermediate'),
                ('SQLite', 0, 'Intermediate'),
                ('Figma', 0, 'Beginner')
            ]
        },
        {
            'title': 'QA Automation Engineer',
            'category': 'Testing & Quality',
            'description': 'Formulate comprehensive automated test suites, end-to-end integration tests, regression checks, and ensure code reliability within CI pipelines.',
            'experience_level': 'Entry to Mid Level',
            'salary_range': '$65,000 - $105,000 / year',
            'learning_overview': 'Master unit testing frameworks in Python, API validation using Postman/requests, test case design, Git branching, and CI/CD test gates.',
            'skills': [
                ('Python', 1, 'Intermediate'),
                ('PyTest', 1, 'Intermediate'),
                ('Git', 1, 'Intermediate'),
                ('REST APIs', 1, 'Intermediate'),
                ('SQL', 1, 'Intermediate'),
                ('Postman', 0, 'Intermediate'),
                ('CI/CD', 0, 'Beginner'),
                ('Linux', 0, 'Beginner'),
                ('Jira', 0, 'Beginner'),
                ('Problem Solving', 0, 'Intermediate')
            ]
        },
        {
            'title': 'Database Administrator & SQL Developer',
            'category': 'Databases',
            'description': 'Administer enterprise relational database management systems, tune query performance, implement backup/recovery, and architect scalable data schemas.',
            'experience_level': 'Entry to Mid Level',
            'salary_range': '$75,000 - $115,000 / year',
            'learning_overview': 'Deepen mastery of SQL schema design, query plan analysis, indexing strategies, PostgreSQL/MySQL administration, and automated backup scripting.',
            'skills': [
                ('SQL', 1, 'Advanced'),
                ('PostgreSQL', 1, 'Advanced'),
                ('MySQL', 1, 'Intermediate'),
                ('Linux', 1, 'Intermediate'),
                ('Git', 1, 'Intermediate'),
                ('Bash', 0, 'Intermediate'),
                ('Python', 0, 'Intermediate'),
                ('Redis', 0, 'Beginner'),
                ('AWS', 0, 'Beginner')
            ]
        }
    ]

    for role_data in roles:
        cursor.execute("SELECT id FROM job_roles WHERE title = ?", (role_data['title'],))
        existing_role = cursor.fetchone()
        if existing_role:
            job_id = existing_role[0]
        else:
            cursor.execute("""
                INSERT INTO job_roles (title, category, description, experience_level, salary_range, learning_overview)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                role_data['title'],
                role_data['category'],
                role_data['description'],
                role_data['experience_level'],
                role_data['salary_range'],
                role_data['learning_overview']
            ))
            job_id = cursor.lastrowid

        # Insert job skills
        for skill_name, is_req, min_prof in role_data['skills']:
            cursor.execute("""
                INSERT OR IGNORE INTO job_skills (job_id, skill_name, is_required, minimum_proficiency, importance_score)
                VALUES (?, ?, ?, ?, ?)
            """, (job_id, skill_name, is_req, min_prof, 1.0 if is_req == 1 else 0.5))

    # 4. Seed a sample student account for demonstration
    cursor.execute("SELECT id FROM users WHERE email = ?", ('student@careerbridge.com',))
    if not cursor.fetchone():
        student_pass_hash = generate_password_hash('Student@123')
        cursor.execute("""
            INSERT INTO users (full_name, email, password_hash, college_name, degree, department, graduation_year, career_goal, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'Alex Morgan',
            'student@careerbridge.com',
            student_pass_hash,
            'Institute of Technology',
            'Bachelor of Engineering',
            'Computer Science & Engineering',
            2025,
            'Aspiring Full-Stack Developer & Python Engineer',
            0
        ))
        student_id = cursor.lastrowid

        # Seed sample skills for Alex
        sample_skills = [
            ('Python', 'Languages', 'Intermediate'),
            ('JavaScript', 'Languages', 'Intermediate'),
            ('HTML', 'Languages', 'Advanced'),
            ('CSS', 'Languages', 'Advanced'),
            ('SQL', 'Languages', 'Beginner'),
            ('Flask', 'Web Dev', 'Beginner'),
            ('Git', 'Tools', 'Intermediate'),
            ('Problem Solving', 'Soft Skills', 'Intermediate')
        ]
        for sk_name, sk_cat, sk_prof in sample_skills:
            cursor.execute("""
                INSERT OR IGNORE INTO user_skills (user_id, skill_name, category, proficiency)
                VALUES (?, ?, ?, ?)
            """, (student_id, sk_name, sk_cat, sk_prof))

    conn.commit()
    print("Database seeding completed successfully.")

if __name__ == '__main__':
    from config import Config
    import os
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    seed_database(conn)
    conn.close()
