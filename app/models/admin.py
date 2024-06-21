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

@admin_bp.route('/admin/manage_customers')
@login_required
def manage_customers():
    if current_user.role not in ['customer_admin', 'superadmin']:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home.home'))

    customers = User.query.filter_by(role='user').all()
    return render_template('manage_customers.html', customers=customers)

@admin_bp.route('/admin/update_customer_field', methods=['POST'])
@login_required
def update_customer_field():
    if current_user.role != 'superadmin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    data = request.json
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400

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
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400

    user_id = data.get('user_id')
    points_to_subtract = int(data.get('points'))

    user = User.query.get(user_id)
    if user:
        user.points -= points_to_subtract
        db.session.commit()
        return jsonify({'status': 'success', 'new_points': user.points})
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

@admin_bp.route('/admin/delete_customer', methods=['POST'])
@login_required
def delete_customer():
    if current_user.role != 'superadmin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    data = request.json
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400

    user_id = data.get('user_id')

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
