from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import db, User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role not in ['superadmin', 'admin']:
        return "Access Denied", 403
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@admin_bp.route('/admin/deduct-points', methods=['POST'])
@login_required
def deduct_points():
    if current_user.role not in ['superadmin', 'admin']:
        return "Access Denied", 403

    user_id = request.form.get('user_id')
    points_to_deduct = int(request.form.get('points'))

    user = User.query.get(user_id)
    if user:
        user.points = max(0, user.points - points_to_deduct)
        db.session.commit()
        flash(f'Successfully deducted {points_to_deduct} points from {user.buyer_name}', 'success')
    else:
        flash('User not found', 'error')

    return redirect(url_for('admin.admin_dashboard'))
