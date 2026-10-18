# CareerBridge 🚀

> **Intelligent Career Navigation & Skill Gap Roadmaps for Tech Students**
> Built with Python Flask, SQLite, HTML5, CSS3, Vanilla JavaScript, Bootstrap 5, and Chart.js.

CareerBridge is a production-ready, modern, and beginner-friendly web application engineered to bridge the gap between academic college studies and real-world tech industry expectations. It extracts technical skills from student resumes locally without paid APIs, calculates mathematical skill gap matches against 12+ pre-seeded tech positions, and automatically generates interactive, step-by-step learning roadmaps with curated resources.

---

## 🌟 Key Features

1. **Modern SaaS UI & Responsive Landing Page:**
   - Indigo & Slate Blue aesthetic with glassmorphism, micro-animations, and dynamic hero statistics.
   - Interactive workflow roadmap and featured tech roles preview.

2. **Student Authentication & Academic Profile:**
   - Secure session-based authentication with Werkzeug password hashing.
   - Detailed academic profile (College, Degree, Department, Expected Graduation Year, Primary Career Target).
   - Profile completeness tracking.

3. **Student Analytics Dashboard:**
   - 5 dynamically calculated database metric cards (Profile Completion %, Total Skills, Recommended Roles, Average Match %, Roadmap Progress %).
   - Chart.js interactive visualizations:
     - **Skill Category Distribution** (Doughnut chart)
     - **Top Role Match Comparison** (Horizontal bar chart)
   - Real-time upcoming milestone tracker with status switcher.
   - Elegant empty-state onboarding for newly created accounts.

4. **Skills Management Module:**
   - 8 Technical Categories: *Languages, Web Dev, Databases, Data Analytics, Cloud, Cybersecurity, Tools, Soft Skills*.
   - 3 Proficiency Tiers: *Beginner, Intermediate, Advanced*.
   - Live client-side instant search and category filter pills.
   - Duplicate entry prevention with database and application validations.
   - Quick modals for adding and updating proficiency levels.

5. **Rule-Based Job Matching Engine & Skill Gap Analysis:**
   - Pre-seeded with 12 realistic industry positions (Python Developer, Full-Stack Developer, Data Analyst, Data Engineer, Frontend Developer, Backend Engineer, Cybersecurity Analyst, Cloud & DevOps Engineer, Machine Learning Engineer, Mobile App Developer, QA Automation Engineer, Database Administrator).
   - Mathematical formula:
     $$\text{Required Match \%} = \left(\frac{\text{Matched Required Skills}}{\text{Total Required Skills}}\right) \times 100$$
   - Visual side-by-side gap analysis comparing matched skills (with proficiency levels) vs missing skills.

6. **Personalized Learning Roadmaps:**
   - Generates sequenced milestone plans targeting missing required and preferred skills.
   - Includes real curated learning documentation (Python Docs, MDN Web Docs, FreeCodeCamp, Scikit-Learn, Docker, SQLBolt, roadmap.sh).
   - Interactive milestone status toggles (*Not Started*, *In Progress*, *Completed*) updating progress bars and counts in real time via AJAX.

7. **Local Resume Analyzer:**
   - Accepts `.pdf` and `.docx` documents under 5 MB.
   - Offline text parsing via `pdfplumber` / `pypdf` and `python-docx` matching against standard skills and alias variants.
   - Review confirmation screen letting students select skills and configure categories/proficiencies before adding to their profile.
   - Zero third-party cloud data leakage — 100% private and offline.

8. **Admin Management Console:**
   - Protected with administrator role checks.
   - Create, edit, and delete job roles.
   - Configure required vs preferred skills for any role.
   - Add new competencies to the global standard skill dictionary.
   - Live student registration metrics and aggregate statistics.

---

## 📁 Repository Structure

```text
CareerBridge/
├── app.py                      # Application entry point and factory
├── config.py                   # Central configuration & constants
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation & setup instructions
├── database/
│   ├── schema.sql              # SQLite relational schema with indexes
│   ├── init_db.py              # Database initialization helper
│   └── seed_data.py            # Pre-seeded admin, roles, skills, and student
├── services/
│   ├── matching_service.py     # Rule-based matching engine & gap analysis
│   ├── resume_service.py       # Local PDF & DOCX text parsing & extraction
│   └── roadmap_service.py      # Roadmap generation & real-time progress engine
├── blueprints/
│   ├── auth.py                 # Registration, login, profile, and security decorators
│   ├── dashboard.py            # Student dashboard metrics & Chart.js payload
│   ├── skills.py               # Skill portfolio management (CRUD)
│   ├── jobs.py                 # Job roles catalog & gap analysis routing
│   ├── roadmap.py              # Personalized roadmaps & AJAX status endpoint
│   ├── resume.py               # Resume upload & import confirmation
│   └── admin.py                # Admin console & role curation
├── templates/
│   ├── base.html               # Base layout, navbar, footer & CDN assets
│   ├── index.html              # Modern landing page & public presentation
│   ├── login.html              # Authentication screen with demo helpers
│   ├── register.html           # Full student registration form
│   ├── dashboard.html          # Student analytics dashboard with Chart.js
│   ├── profile.html            # Profile settings & password change
│   ├── skills.html             # Skill cards grid, filtering & modals
│   ├── jobs.html               # Job roles catalog with match percentages
│   ├── job_detail.html         # Detailed role description & skill matrix
│   ├── skill_gap.html          # In-depth matched vs missing comparison
│   ├── roadmap.html            # Structured timeline with AJAX updates
│   ├── resume_analyzer.html    # Drag-and-drop file upload & skill review
│   └── admin_dashboard.html    # Admin management portal
└── static/
    ├── css/style.css           # Indigo/Slate SaaS theme & responsive tokens
    └── js/main.js              # Client interactivity, AJAX, & file handling
```

---

## 🔑 Pre-Seeded Default Accounts

| Role | Email | Password | Access |
|---|---|---|---|
| **Platform Administrator** | `admin@careerbridge.com` | `Admin@123` | Full Admin Console & Role Curation |
| **Demo Student** | `student@careerbridge.com` | `Student@123` | Pre-populated profile with 8 skills & matches |

*You can also click **Get Started** on the landing page to register any number of new student accounts.*

---

## 💻 Windows Command Prompt Setup Instructions

Follow these step-by-step instructions to run CareerBridge on Windows:

### Step 1: Open Windows Command Prompt
Press `Win + R`, type `cmd`, and press **Enter**. Then navigate to your project directory:
```cmd
cd C:\Users\Lithiga\Desktop\CareerBridge
```

### Step 2: (Optional but Recommended) Create and Activate Virtual Environment
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Required Python Packages
```cmd
pip install -r requirements.txt
```
*Dependencies installed: `Flask`, `Werkzeug`, `pypdf`, `pdfplumber`, `python-docx`.*

### Step 4: Initialize and Seed Local Database
```cmd
python database/init_db.py
```
*This command executes `schema.sql` and populates the database with the standard skill dictionary, 12 realistic job roles, default admin, and a demo student.*

### Step 5: Start the Web Application
```cmd
python app.py
```

### Step 6: Access CareerBridge in Your Web Browser
Open your favorite browser and visit:
```text
http://127.0.0.1:5000
```

---

## 🧪 Testing the End-to-End Workflow

1. **Sign In as Demo Student:**
   - Log in using `student@careerbridge.com` and `Student@123`.
   - View your Dashboard metrics and observe the **Category Distribution** and **Top Role Match** Chart.js graphs.
2. **Explore Roles & Skill Gaps:**
   - Navigate to **Job Roles** in the top navigation bar.
   - Click **Skill Gap** on *Python Developer* or *Full-Stack Web Developer*.
   - Review your matched competencies vs missing requirements.
3. **Generate & Track a Roadmap:**
   - Click **Generate Personalized Roadmap Now**.
   - Change the milestone status from *Not Started* to *In Progress* or *Completed*. Notice how the overall roadmap progress bar recalculates dynamically.
4. **Test Resume Analyzer:**
   - Go to **Resume Analyzer** and upload a `.pdf` or `.docx` resume.
   - Review detected skills on the confirmation screen, set proficiency, and click **Confirm & Import Skills**.
5. **Admin Portal:**
   - Sign in as `admin@careerbridge.com` / `Admin@123`.
   - Access the **Admin Portal** from the navbar.
   - Add new job roles, assign required skills, and monitor registered student statistics.
