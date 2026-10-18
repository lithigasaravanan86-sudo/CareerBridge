import datetime

SKILL_LEARNING_RESOURCES = {
    'python': {
        'title': 'Master Modern Python 3 & Object-Oriented Design',
        'desc': 'Understand Python data structures, list comprehensions, decorators, generators, error handling, and object-oriented programming.',
        'resource_title': 'Python Official Tutorial & FreeCodeCamp Python Course',
        'resource_url': 'https://docs.python.org/3/tutorial/',
        'hours': 15
    },
    'javascript': {
        'title': 'Core JavaScript ES6+, Async/Await & DOM Mastery',
        'desc': 'Deep dive into asynchronous JavaScript (Promises, async/await), closures, prototypes, event delegation, and browser APIs.',
        'resource_title': 'MDN Web Docs - JavaScript Guide',
        'resource_url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
        'hours': 18
    },
    'typescript': {
        'title': 'TypeScript Type Safety & Enterprise Architecture',
        'desc': 'Master interfaces, generics, utility types, unions, and configuring tsconfig for robust web development.',
        'resource_title': 'TypeScript Official Handbook',
        'resource_url': 'https://www.typescriptlang.org/docs/handbook/intro.html',
        'hours': 12
    },
    'html': {
        'title': 'Semantic HTML5 & Accessibility Standards (WCAG)',
        'desc': 'Learn semantic document structuring, accessible forms, ARIA attributes, and SEO markup best practices.',
        'resource_title': 'MDN HTML Basics & Semantics',
        'resource_url': 'https://developer.mozilla.org/en-US/docs/Learn/HTML',
        'hours': 8
    },
    'css': {
        'title': 'Modern CSS3, Flexbox, Grid & Responsive Layouts',
        'desc': 'Master CSS Grid, Flexbox layouts, media queries, CSS custom variables, and keyframe animations.',
        'resource_title': 'CSS-Tricks & MDN CSS Modules',
        'resource_url': 'https://developer.mozilla.org/en-US/docs/Learn/CSS',
        'hours': 12
    },
    'react': {
        'title': 'React Component Lifecycle, Hooks & State Management',
        'desc': 'Build scalable components using useState, useEffect, custom hooks, context API, and component memoization.',
        'resource_title': 'Official React Documentation & Interactive Tutorial',
        'resource_url': 'https://react.dev/learn',
        'hours': 20
    },
    'next.js': {
        'title': 'Next.js App Router, SSR & Full-Stack Capabilities',
        'desc': 'Learn server-side rendering (SSR), static site generation (SSG), API routes, and Server Actions.',
        'resource_title': 'Next.js Official Learn Course',
        'resource_url': 'https://nextjs.org/learn',
        'hours': 15
    },
    'node.js': {
        'title': 'Node.js Runtime, Event Loop & File System Operations',
        'desc': 'Understand the V8 engine, event loop, streams, buffers, npm ecosystem, and non-blocking I/O.',
        'resource_title': 'Node.js Official Documentation & Learn Guides',
        'resource_url': 'https://nodejs.org/en/learn',
        'hours': 16
    },
    'express.js': {
        'title': 'RESTful API Engineering with Express.js',
        'desc': 'Build REST APIs with routing, middleware architecture, request validation, authentication, and error handlers.',
        'resource_title': 'Express.js Getting Started & Guide',
        'resource_url': 'https://expressjs.com/en/starter/installing.html',
        'hours': 12
    },
    'flask': {
        'title': 'Lightweight Web Services & Blueprints with Python Flask',
        'desc': 'Architect scalable Flask applications with Blueprints, Jinja2 templating, session auth, and SQLite/SQLAlchemy.',
        'resource_title': 'Flask Official User Guide',
        'resource_url': 'https://flask.palletsprojects.com/',
        'hours': 14
    },
    'sql': {
        'title': 'Relational Database Queries, Joins, Indexing & Aggregation',
        'desc': 'Master SELECT queries, multi-table JOINs, subqueries, GROUP BY, window functions, and database schema normalization.',
        'resource_title': 'SQLBolt - Interactive SQL Lessons',
        'resource_url': 'https://sqlbolt.com/',
        'hours': 14
    },
    'postgresql': {
        'title': 'PostgreSQL Administration, Constraints & Advanced Types',
        'desc': 'Design robust relational schemas, JSONB columns, foreign key constraints, indexes, and performance query plans.',
        'resource_title': 'PostgreSQL Tutorial & Documentation',
        'resource_url': 'https://www.postgresqltutorial.com/',
        'hours': 15
    },
    'mongodb': {
        'title': 'MongoDB Document Modeling & Aggregation Pipelines',
        'desc': 'Understand NoSQL document schemas, indexing in collections, CRUD operations, and Mongoose ODM.',
        'resource_title': 'MongoDB University & Manual',
        'resource_url': 'https://www.mongodb.com/docs/manual/',
        'hours': 12
    },
    'redis': {
        'title': 'In-Memory Caching & Session Stores with Redis',
        'desc': 'Implement fast in-memory key-value caching, Pub/Sub, rate limiting, and session persistence.',
        'resource_title': 'Redis Official Documentation',
        'resource_url': 'https://redis.io/docs/latest/',
        'hours': 8
    },
    'git': {
        'title': 'Git Version Control, Branching & Collaborative Workflows',
        'desc': 'Master git commit, branching, merging, rebasing, conflict resolution, and GitHub pull request best practices.',
        'resource_title': 'Git-SCM Official Pro Git Book',
        'resource_url': 'https://git-scm.com/book/en/v2',
        'hours': 8
    },
    'docker': {
        'title': 'Containerization Fundamentals & Docker Compose',
        'desc': 'Write multi-stage Dockerfiles, manage volume persistence, expose ports, and run multi-container applications.',
        'resource_title': 'Docker Official Getting Started Guide',
        'resource_url': 'https://docs.docker.com/get-started/',
        'hours': 14
    },
    'kubernetes': {
        'title': 'Container Orchestration with Kubernetes (K8s)',
        'desc': 'Deploy Pods, Deployments, Services, ConfigMaps, and Ingress controllers for scalable cloud infrastructure.',
        'resource_title': 'Kubernetes Basics & Tutorials',
        'resource_url': 'https://kubernetes.io/docs/tutorials/kubernetes-basics/',
        'hours': 20
    },
    'aws': {
        'title': 'AWS Cloud Fundamentals: EC2, S3, IAM & CloudFront',
        'desc': 'Provision virtual servers, configure S3 buckets, manage IAM policies, and deploy web applications to AWS.',
        'resource_title': 'AWS Skill Builder - Cloud Essentials',
        'resource_url': 'https://aws.amazon.com/training/digital/',
        'hours': 22
    },
    'ci/cd': {
        'title': 'Continuous Integration & Continuous Deployment Pipelines',
        'desc': 'Set up automated test suites, linting, and production deployment pipelines using GitHub Actions.',
        'resource_title': 'GitHub Actions Documentation & Guides',
        'resource_url': 'https://docs.github.com/en/actions',
        'hours': 10
    },
    'linux': {
        'title': 'Linux Command Line, Shell Scripting & Server Administration',
        'desc': 'Master the bash terminal, file permissions (chmod/chown), process monitoring (ps/top), cron jobs, and SSH.',
        'resource_title': 'Linux Journey - Free CLI Tutorial',
        'resource_url': 'https://linuxjourney.com/',
        'hours': 12
    },
    'pandas': {
        'title': 'Data Wrangling, Cleaning & Analysis with Pandas',
        'desc': 'Manipulate DataFrames, clean missing values, handle datetime series, merge datasets, and compute aggregate metrics.',
        'resource_title': 'Pandas Official 10-Minute Guide & Tutorials',
        'resource_url': 'https://pandas.pydata.org/docs/user_guide/10min.html',
        'hours': 15
    },
    'numpy': {
        'title': 'Numerical Computing & Vectorized Array Operations with NumPy',
        'desc': 'Understand multi-dimensional arrays, broadcasting, linear algebra operations, and mathematical computations.',
        'resource_title': 'NumPy User Guide & Quickstart',
        'resource_url': 'https://numpy.org/doc/stable/user/quickstart.html',
        'hours': 10
    },
    'tableau': {
        'title': 'Visual Business Intelligence Dashboards in Tableau',
        'desc': 'Create interactive executive dashboards, calculated fields, parameters, and geospatial visualizations.',
        'resource_title': 'Tableau Free Training Videos & Docs',
        'resource_url': 'https://www.tableau.com/learn/training',
        'hours': 14
    },
    'power bi': {
        'title': 'Interactive Business Analytics with Microsoft Power BI',
        'desc': 'Import disparate data models, write DAX calculations, and build dynamic cross-filtering report dashboards.',
        'resource_title': 'Microsoft Power BI Guided Learning',
        'resource_url': 'https://learn.microsoft.com/en-us/power-bi/',
        'hours': 14
    },
    'excel': {
        'title': 'Advanced Excel for Business & Financial Analytics',
        'desc': 'Master XLOOKUP/VLOOKUP, Pivot Tables, nested formulas, conditional formatting, and data validation.',
        'resource_title': 'Microsoft Excel Video Training',
        'resource_url': 'https://support.microsoft.com/en-us/office/excel-video-training-9bc05390-e94c-46af-a5b3-d7c22f6990bb',
        'hours': 10
    },
    'machine learning': {
        'title': 'Supervised & Unsupervised Machine Learning Fundamentals',
        'desc': 'Implement classification, regression, clustering algorithms, and model evaluation metrics with Scikit-Learn.',
        'resource_title': 'Scikit-Learn Machine Learning Tutorials',
        'resource_url': 'https://scikit-learn.org/stable/tutorial/index.html',
        'hours': 25
    },
    'network security': {
        'title': 'Network Security Architecture, Firewalls & Protocols',
        'desc': 'Understand OSI & TCP/IP models, subnetting, DNS security, SSL/TLS handshakes, and firewall configuration.',
        'resource_title': 'Cisco Networking Academy & Cybrary Network Security',
        'resource_url': 'https://www.cybrary.it/',
        'hours': 18
    },
    'wireshark': {
        'title': 'Packet Analysis & Traffic Forensics with Wireshark',
        'desc': 'Capture network packets, apply display filters, analyze HTTP/DNS/TCP streams, and diagnose anomalies.',
        'resource_title': 'Wireshark User Guide & Packet Analysis Guide',
        'resource_url': 'https://www.wireshark.org/docs/',
        'hours': 10
    },
    'owasp top 10': {
        'title': 'Web Application Security & OWASP Top 10 Mitigation',
        'desc': 'Analyze and defend against SQL Injection, Cross-Site Scripting (XSS), Broken Authentication, and SSRF.',
        'resource_title': 'OWASP Top 10 Official Documentation',
        'resource_url': 'https://owasp.org/www-project-top-ten/',
        'hours': 14
    },
    'pytest': {
        'title': 'Automated Unit & Integration Testing with PyTest',
        'desc': 'Write test assertions, parameterized tests, test fixtures, mocks, and calculate code coverage.',
        'resource_title': 'PyTest Documentation & Tutorial',
        'resource_url': 'https://docs.pytest.org/',
        'hours': 10
    },
    'rest apis': {
        'title': 'API Design Principles, HTTP Verbs & Status Codes',
        'desc': 'Design consistent endpoints, query filtering, pagination, JSON serialization, and OpenAPI/Swagger specs.',
        'resource_title': 'REST API Tutorial & Best Practices',
        'resource_url': 'https://restfulapi.net/',
        'hours': 10
    }
}

def generate_roadmap_for_role(user_id, job_id, conn):
    """
    Generates or resets an actionable personalized learning roadmap for a student and target job role.
    Targeting missing skills first, then proficiency reinforcement, ending with a capstone project.
    """
    cursor = conn.cursor()

    # Get Job Details
    cursor.execute("SELECT * FROM job_roles WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    if not job:
        return None

    # Get User Details
    cursor.execute("SELECT full_name FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    # Get Skill Gap details
    from services.matching_service import get_skill_gap_for_job
    gap_data = get_skill_gap_for_job(user_id, job_id, conn)

    # Check if a roadmap already exists for this job and user
    cursor.execute("SELECT id FROM user_roadmaps WHERE user_id = ? AND job_id = ?", (user_id, job_id))
    existing_roadmap = cursor.fetchone()

    if existing_roadmap:
        roadmap_id = existing_roadmap['id']
        # Clear existing items to regenerate fresh updated plan
        cursor.execute("DELETE FROM roadmap_items WHERE roadmap_id = ?", (roadmap_id,))
        cursor.execute("UPDATE user_roadmaps SET updated_at = CURRENT_TIMESTAMP, status = 'In Progress' WHERE id = ?", (roadmap_id,))
    else:
        roadmap_title = f"{job['title']} Career Readiness Roadmap"
        cursor.execute("""
            INSERT INTO user_roadmaps (user_id, job_id, title, status)
            VALUES (?, ?, ?, 'In Progress')
        """, (user_id, job_id, roadmap_title))
        roadmap_id = cursor.lastrowid

    # Create Roadmap Items
    order = 1

    # 1. First add milestones for MISSING REQUIRED skills
    missing_required = [s for s in gap_data['match']['missing_skills'] if s['is_required']]
    # 2. Then add milestones for MISSING PREFERRED skills
    missing_preferred = [s for s in gap_data['match']['missing_skills'] if not s['is_required']]
    # 3. Then add milestones for MATCHED skills with a PROFICIENCY GAP
    matched_with_gap = [s for s in gap_data['match']['matched_skills'] if s['proficiency_gap']]

    roadmap_queue = []

    for item in missing_required:
        roadmap_queue.append({
            'skill_name': item['skill_name'],
            'type': 'Required Skill Mastery',
            'min_prof': item['minimum_proficiency']
        })

    for item in missing_preferred:
        roadmap_queue.append({
            'skill_name': item['skill_name'],
            'type': 'Preferred Advantage Skill',
            'min_prof': item['minimum_proficiency']
        })

    for item in matched_with_gap:
        roadmap_queue.append({
            'skill_name': item['skill_name'],
            'type': 'Proficiency Level Up',
            'min_prof': item['minimum_proficiency']
        })

    # If the user has 0 gaps, add advanced mastery and portfolio tasks!
    if not roadmap_queue:
        roadmap_queue.append({
            'skill_name': 'Advanced Architecture',
            'type': 'System Design & Optimization',
            'min_prof': 'Advanced'
        })

    for entry in roadmap_queue:
        sk_key = entry['skill_name'].lower().strip()
        res_info = SKILL_LEARNING_RESOURCES.get(sk_key, {
            'title': f"Master {entry['skill_name']} for {job['title']}",
            'desc': f"Study foundational and applied principles of {entry['skill_name']}. Implement hands-on exercises and integrate into small modules.",
            'resource_title': f"{entry['skill_name']} Technical Documentation & Learning Guide",
            'resource_url': 'https://roadmap.sh/',
            'hours': 12
        })

        milestone_title = f"Phase {order}: {entry['skill_name']} ({entry['type']})"
        cursor.execute("""
            INSERT INTO roadmap_items 
            (roadmap_id, skill_name, milestone_title, description, resource_title, resource_url, estimated_hours, status, order_index)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Not Started', ?)
        """, (
            roadmap_id,
            entry['skill_name'],
            milestone_title,
            res_info['desc'],
            res_info['resource_title'],
            res_info['resource_url'],
            res_info['hours'],
            order
        ))
        order += 1

    # Final Capstone Project Milestone
    capstone_title = f"Phase {order}: Final Capstone Project for {job['title']}"
    capstone_desc = (
        f"Design and deliver an end-to-end production-quality portfolio project demonstrating your acquired skills "
        f"for {job['title']}. Document architecture, write automated tests, and publish to GitHub."
    )
    cursor.execute("""
        INSERT INTO roadmap_items 
        (roadmap_id, skill_name, milestone_title, description, resource_title, resource_url, estimated_hours, status, order_index)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Not Started', ?)
    """, (
        roadmap_id,
        'Portfolio Project',
        capstone_title,
        capstone_desc,
        'GitHub Project Portfolio Best Practices',
        'https://github.com/explore',
        25,
        order
    ))

    conn.commit()
    return roadmap_id

def get_roadmap_details(roadmap_id, user_id, conn):
    """
    Fetches full roadmap details including items, progress percentage, and statistics.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, j.title as job_title, j.category as job_category, j.description as job_description, j.salary_range
        FROM user_roadmaps r
        JOIN job_roles j ON r.job_id = j.id
        WHERE r.id = ? AND r.user_id = ?
    """, (roadmap_id, user_id))
    roadmap = cursor.fetchone()

    if not roadmap:
        return None

    cursor.execute("""
        SELECT * FROM roadmap_items 
        WHERE roadmap_id = ? 
        ORDER BY order_index ASC
    """, (roadmap_id,))
    items = cursor.fetchall()

    total_items = len(items)
    completed_items = len([i for i in items if i['status'] == 'Completed'])
    in_progress_items = len([i for i in items if i['status'] == 'In Progress'])
    not_started_items = len([i for i in items if i['status'] == 'Not Started'])

    total_hours = sum(i['estimated_hours'] for i in items)
    completed_hours = sum(i['estimated_hours'] for i in items if i['status'] == 'Completed')

    progress_pct = round((completed_items / total_items) * 100, 1) if total_items > 0 else 0.0

    return {
        'roadmap': dict(roadmap),
        'items': [dict(i) for i in items],
        'total_items': total_items,
        'completed_items': completed_items,
        'in_progress_items': in_progress_items,
        'not_started_items': not_started_items,
        'total_hours': total_hours,
        'completed_hours': completed_hours,
        'progress_pct': progress_pct
    }

def update_roadmap_item_status(item_id, user_id, new_status, conn):
    """
    Updates the status of a milestone item, updating completion timestamp and overall roadmap status.
    """
    valid_statuses = ['Not Started', 'In Progress', 'Completed']
    if new_status not in valid_statuses:
        return False, "Invalid status"

    cursor = conn.cursor()
    # Verify ownership
    cursor.execute("""
        SELECT i.id, i.roadmap_id 
        FROM roadmap_items i
        JOIN user_roadmaps r ON i.roadmap_id = r.id
        WHERE i.id = ? AND r.user_id = ?
    """, (item_id, user_id))
    item = cursor.fetchone()

    if not item:
        return False, "Item not found or unauthorized"

    roadmap_id = item['roadmap_id']
    completed_at = datetime.datetime.now().isoformat() if new_status == 'Completed' else None

    cursor.execute("""
        UPDATE roadmap_items 
        SET status = ?, completed_at = ?
        WHERE id = ?
    """, (new_status, completed_at, item_id))

    # Check overall roadmap completion
    cursor.execute("SELECT status FROM roadmap_items WHERE roadmap_id = ?", (roadmap_id,))
    all_items = cursor.fetchall()
    total = len(all_items)
    completed = len([i for i in all_items if i['status'] == 'Completed'])

    overall_status = 'Completed' if (total > 0 and completed == total) else 'In Progress'
    cursor.execute("""
        UPDATE user_roadmaps 
        SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (overall_status, roadmap_id))

    conn.commit()

    progress_pct = round((completed / total) * 100, 1) if total > 0 else 0.0

    return True, {
        'item_id': item_id,
        'status': new_status,
        'progress_pct': progress_pct,
        'completed_items': completed,
        'total_items': total,
        'roadmap_status': overall_status
    }

def get_user_all_roadmaps(user_id, conn):
    """Returns all roadmaps generated by a user with summary progress."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, j.title as job_title, j.category as job_category,
               (SELECT COUNT(*) FROM roadmap_items WHERE roadmap_id = r.id) as total_items,
               (SELECT COUNT(*) FROM roadmap_items WHERE roadmap_id = r.id AND status = 'Completed') as completed_items
        FROM user_roadmaps r
        JOIN job_roles j ON r.job_id = j.id
        WHERE r.user_id = ?
        ORDER BY r.updated_at DESC
    """, (user_id,))
    rows = cursor.fetchall()

    roadmaps = []
    for r in rows:
        d = dict(r)
        total = d['total_items'] or 0
        comp = d['completed_items'] or 0
        d['progress_pct'] = round((comp / total) * 100, 1) if total > 0 else 0.0
        roadmaps.append(d)

    return roadmaps
