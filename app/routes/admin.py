import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.models import db, User, PromotionCode
from app.forms import AdminForm
import pandas as pd
import logging

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'superadmin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home.home'))

    return render_template('admin_dashboard.html')

@admin_bp.route('/admin/manage_hr_admins', methods=['GET', 'POST'])
@login_required
def manage_hr_admins():
    if current_user.role != 'superadmin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home.home'))

    form = AdminForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = 'hr_admin'

        hashed_password = generate_password_hash(password)
        new_admin = User(company_name="Admin Company", buyer_name=username, phone_number=username, password_hash=hashed_password, role=role)
        db.session.add(new_admin)
        db.session.commit()

        flash('HR Admin created successfully!', 'success')
        return redirect(url_for('admin.manage_hr_admins'))

    admins = User.query.filter_by(role='hr_admin').all()
    return render_template('manage_hr_admins.html', form=form, admins=admins)

@admin_bp.route('/admin/manage_customer_admins', methods=['GET', 'POST'])
@login_required
def manage_customer_admins():
    if current_user.role != 'superadmin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home.home'))

    form = AdminForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = 'customer_admin'

        hashed_password = generate_password_hash(password)
        new_admin = User(company_name="Admin Company", buyer_name=username, phone_number=username, password_hash=hashed_password, role=role)
        db.session.add(new_admin)
        db.session.commit()

        flash('Customer Admin created successfully!', 'success')
        return redirect(url_for('admin.manage_customer_admins'))

    admins = User.query.filter_by(role='customer_admin').all()
    return render_template('manage_customer_admins.html', form=form, admins=admins)

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

    try:
        data = request.json
        if not data:
            return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400

        user_id = data.get('user_id')
        fields = data.get('fields')

        user = User.query.get(user_id)
        if user:
            for field, value in fields.items():
                setattr(user, field, value)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
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

@admin_bp.route('/admin/get_customer/<int:user_id>')
@login_required
def get_customer(user_id):
    if current_user.role != 'superadmin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    user = User.query.get(user_id)
    if user:
        return jsonify({
            'status': 'success',
            'customer': {
                'id': user.id,
                'company_name': user.company_name,
                'buyer_name': user.buyer_name,
                'phone_number': user.phone_number,
                'points': user.points
            }
        })
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

@admin_bp.route('/admin/upload_promotion_codes', methods=['POST'])
@login_required
def upload_promotion_codes():
    if current_user.role != 'superadmin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    if 'file' not in request.files:
        logging.error('No file part')
        return jsonify({'status': 'error', 'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        logging.error('No selected file')
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400

    if file:
        try:
            content = file.read().decode('utf-8')
            codes = content.splitlines()

            # Đường dẫn tới file CSV lưu trữ mã khuyến mãi
            csv_file = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'promotioncodelist.csv')

            # Đọc dữ liệu CSV hiện tại
            if os.path.exists(csv_file):
                existing_df = pd.read_csv(csv_file)
            else:
                existing_df = pd.DataFrame(columns=['code', 'used'])

            # Thêm các mã khuyến mãi mới vào DataFrame
            for code in codes:
                if code not in existing_df['code'].values:
                    new_row = pd.DataFrame({'code': [code], 'used': [False]})
                    existing_df = pd.concat([existing_df, new_row], ignore_index=True)

            # Lưu DataFrame vào file CSV
            existing_df.to_csv(csv_file, index=False)
            logging.info('Promotion codes uploaded successfully')
            return jsonify({'status': 'success'})
        except Exception as e:
            logging.error(f'Error processing file: {str(e)}')
            return jsonify({'status': 'error', 'message': 'File processing error'}), 500
    return jsonify({'status': 'error', 'message': 'File processing error'}), 500
