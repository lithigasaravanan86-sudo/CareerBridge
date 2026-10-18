import os
import unittest
import json
from app import create_app
from database.init_db import init_db, get_db_connection

class CareerBridgeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_01_landing_page(self):
        """Test landing page loads with HTTP 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CareerBridge', response.data)
        self.assertIn(b'Curated Job Roles', response.data)

    def test_02_login_and_dashboard(self):
        """Test authentication and dashboard metrics."""
        # 1. Login with demo student
        login_res = self.client.post('/login', data={
            'email': 'student@careerbridge.com',
            'password': 'Student@123'
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertIn(b'Alex Morgan', login_res.data)
        self.assertIn(b'Student Dashboard', login_res.data)

        # 2. Access Dashboard directly
        dash_res = self.client.get('/dashboard')
        self.assertEqual(dash_res.status_code, 200)
        self.assertIn(b'Total Skills', dash_res.data)
        self.assertIn(b'Matching Roles', dash_res.data)

    def test_03_skills_module(self):
        """Test adding, viewing, and deleting skills."""
        # Login
        self.client.post('/login', data={'email': 'student@careerbridge.com', 'password': 'Student@123'})

        # Add a new skill
        add_res = self.client.post('/skills/add', data={
            'skill_name': 'Docker',
            'category': 'Cloud',
            'proficiency': 'Intermediate'
        }, follow_redirects=True)
        self.assertEqual(add_res.status_code, 200)
        self.assertIn(b'Docker', add_res.data)

        # Check duplicate skill prevention
        dup_res = self.client.post('/skills/add', data={
            'skill_name': 'Docker',
            'category': 'Cloud',
            'proficiency': 'Advanced'
        }, follow_redirects=True)
        self.assertEqual(dup_res.status_code, 200)
        self.assertIn(b'already in your skills profile', dup_res.data)

    def test_04_jobs_and_skill_gap(self):
        """Test job roles catalog and skill gap calculations."""
        self.client.post('/login', data={'email': 'student@careerbridge.com', 'password': 'Student@123'})

        # Jobs listing
        jobs_res = self.client.get('/jobs')
        self.assertEqual(jobs_res.status_code, 200)
        self.assertIn(b'Python Developer', jobs_res.data)

        # Job detail
        detail_res = self.client.get('/jobs/1')
        self.assertEqual(detail_res.status_code, 200)
        self.assertIn(b'Role Details', detail_res.data)

        # Skill gap
        gap_res = self.client.get('/jobs/1/skill-gap')
        self.assertEqual(gap_res.status_code, 200)
        self.assertIn(b'Skill Gap Analysis', gap_res.data)
        self.assertIn(b'Matched Skills', gap_res.data)

    def test_05_roadmap_generation_and_ajax_update(self):
        """Test roadmap creation and AJAX milestone update."""
        self.client.post('/login', data={'email': 'student@careerbridge.com', 'password': 'Student@123'})

        # Generate roadmap for job role 1
        gen_res = self.client.post('/roadmap/generate/1', follow_redirects=True)
        self.assertEqual(gen_res.status_code, 200)
        self.assertIn(b'Personalized Career Roadmaps', gen_res.data)

        # Get the first item id
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM roadmap_items LIMIT 1")
        item_id = cursor.fetchone()[0]
        conn.close()

        # Update status via AJAX endpoint
        ajax_res = self.client.post(
            f'/roadmap/item/{item_id}/status',
            data=json.dumps({'status': 'Completed'}),
            content_type='application/json'
        )
        self.assertEqual(ajax_res.status_code, 200)
        data = json.loads(ajax_res.data.decode('utf-8'))
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['status'], 'Completed')

    def test_06_admin_portal(self):
        """Test admin authentication and management capabilities."""
        # Login as admin
        admin_login = self.client.post('/login', data={
            'email': 'admin@careerbridge.com',
            'password': 'Admin@123'
        }, follow_redirects=True)
        self.assertEqual(admin_login.status_code, 200)

        # Access admin console
        admin_res = self.client.get('/admin/dashboard')
        self.assertEqual(admin_res.status_code, 200)
        self.assertIn(b'Platform Administration', admin_res.data)
        self.assertIn(b'Configured Job Roles', admin_res.data)

    def test_07_student_registration(self):
        """Test new user registration."""
        import time
        unique_email = f"candidate_{int(time.time()*1000)}@college.edu"
        reg_res = self.client.post('/register', data={
            'full_name': 'Test Candidate',
            'email': unique_email,
            'password': 'Password@123',
            'confirm_password': 'Password@123',
            'college_name': 'Apex Engineering College',
            'degree': 'B.Tech',
            'department': 'Computer Science',
            'graduation_year': '2026',
            'career_goal': 'Cloud Engineer'
        }, follow_redirects=True)
        self.assertEqual(reg_res.status_code, 200)
        self.assertIn(b'Test Candidate', reg_res.data)
        self.assertIn(b'Dashboard', reg_res.data)

if __name__ == '__main__':
    unittest.main()
