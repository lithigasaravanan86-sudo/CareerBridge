from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from blueprints.auth import login_required
from database.init_db import get_db_connection
from services.roadmap_service import (
    generate_roadmap_for_role,
    get_roadmap_details,
    update_roadmap_item_status,
    get_user_all_roadmaps
)

roadmap_bp = Blueprint('roadmap', __name__)

@roadmap_bp.route('/roadmap')
@login_required
def index():
    user_id = session['user_id']
    conn = get_db_connection()

    all_roadmaps = get_user_all_roadmaps(user_id, conn)

    if not all_roadmaps:
        conn.close()
        # Direct to roadmap view with empty state
        return render_template('roadmap.html', current_roadmap=None, all_roadmaps=[], items=[])

    # If active roadmap id is requested via query param, use it; else use the first one
    active_id = request.args.get('id', type=int)
    if not active_id or not any(r['id'] == active_id for r in all_roadmaps):
        active_id = all_roadmaps[0]['id']

    details = get_roadmap_details(active_id, user_id, conn)
    conn.close()

    if not details:
        flash('Roadmap details could not be loaded.', 'warning')
        return redirect(url_for('jobs.index'))

    return render_template(
        'roadmap.html',
        current_roadmap=details['roadmap'],
        items=details['items'],
        stats=details,
        all_roadmaps=all_roadmaps,
        active_id=active_id
    )

@roadmap_bp.route('/roadmap/generate/<int:job_id>', methods=['POST'])
@login_required
def generate(job_id):
    user_id = session['user_id']
    conn = get_db_connection()

    try:
        roadmap_id = generate_roadmap_for_role(user_id, job_id, conn)
        if roadmap_id:
            flash('Your personalized career roadmap has been generated successfully!', 'success')
            return redirect(url_for('roadmap.index', id=roadmap_id))
        else:
            flash('Job role not found.', 'danger')
            return redirect(url_for('jobs.index'))
    except Exception as e:
        flash(f'Error generating roadmap: {e}', 'danger')
        return redirect(url_for('jobs.index'))
    finally:
        conn.close()

@roadmap_bp.route('/roadmap/item/<int:item_id>/status', methods=['POST'])
@login_required
def update_status(item_id):
    user_id = session['user_id']
    data = request.get_json() or {}
    new_status = data.get('status') or request.form.get('status')

    if not new_status:
        return jsonify({'success': False, 'message': 'Missing status'}), 400

    conn = get_db_connection()
    success, result = update_roadmap_item_status(item_id, user_id, new_status, conn)
    conn.close()

    if success:
        return jsonify({
            'success': True,
            'data': result
        })
    else:
        return jsonify({
            'success': False,
            'message': result
        }), 400

@roadmap_bp.route('/roadmap/delete/<int:roadmap_id>', methods=['POST'])
@login_required
def delete(roadmap_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM user_roadmaps WHERE id = ? AND user_id = ?", (roadmap_id, user_id))
    rm = cursor.fetchone()

    if rm:
        cursor.execute("DELETE FROM user_roadmaps WHERE id = ?", (roadmap_id,))
        conn.commit()
        flash('Roadmap successfully removed.', 'info')
    else:
        flash('Roadmap not found.', 'warning')

    conn.close()
    return redirect(url_for('roadmap.index'))
