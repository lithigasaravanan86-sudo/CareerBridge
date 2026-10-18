import os
from flask import Flask, render_template, session, redirect, url_for
from config import Config
from database.init_db import init_db, get_db_connection

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize SQLite database if it doesn't exist
    if not os.path.exists(app.config['DATABASE_PATH']):
        print("Database not found. Initializing CareerBridge database...")
        init_db()

    # Register Blueprints
    from blueprints.auth import auth_bp
    from blueprints.dashboard import dashboard_bp
    from blueprints.skills import skills_bp
    from blueprints.jobs import jobs_bp
    from blueprints.roadmap import roadmap_bp
    from blueprints.resume import resume_bp
    from blueprints.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(roadmap_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(admin_bp)

    # Global Context Processor
    @app.context_processor
    def inject_global_context():
        current_user = None
        if 'user_id' in session:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id, full_name, email, is_admin, career_goal FROM users WHERE id = ?", (session['user_id'],))
                row = cursor.fetchone()
                if row:
                    current_user = dict(row)
                conn.close()
            except Exception:
                current_user = None

        return {
            'current_user': current_user,
            'is_authenticated': 'user_id' in session,
            'is_admin': session.get('is_admin', False)
        }

    # Favicon Route
    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('favicon.svg')

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_title="404 - Page Not Found", error_msg="The page you requested could not be located."), 404

    @app.errorhandler(413)
    def file_too_large(e):
        return render_template('base.html', error_title="413 - File Too Large", error_msg="The uploaded file exceeds the 5MB size limit. Please upload a smaller document."), 413

    @app.errorhandler(500)
    def server_error(e):
        return render_template('base.html', error_title="500 - Server Error", error_msg="An unexpected error occurred. Please try again or check the terminal logs."), 500

    return app

app = create_app()

if __name__ == '__main__':
    # Run locally on port 5000
    print("Starting CareerBridge Web Application on http://127.0.0.1:5000 ...")
    app.run(debug=True, host='127.0.0.1', port=5000)
