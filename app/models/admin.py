from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return "Access Denied", 403
    return render_template('admin_dashboard.html')
