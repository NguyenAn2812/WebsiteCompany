from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.models import db, User
from app.forms import AdminForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return "Access Denied", 403
    return render_template('admin_dashboard.html')
@admin_bp.route('/admin/update_customer_field', methods=['POST'])
@login_required
def update_customer_field():
    if current_user.role not in ['customer_admin', 'superadmin']:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    data = request.json
    user_id = data.get('user_id')
    field = data.get('field')
    value = data.get('value')

    user = User.query.get(user_id)
    if user:
        setattr(user, field, value)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

@admin_bp.route('/admin/subtract_points', methods=['POST'])
@login_required
def subtract_points():
    if current_user.role not in ['customer_admin', 'superadmin']:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    data = request.json
    user_id = data.get('user_id')

    user = User.query.get(user_id)
    if user:
        user.points -= 1
        db.session.commit()
        return jsonify({'status': 'success', 'new_points': user.points})
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404