from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User
from app.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        company_name = form.company_name.data
        buyer_name = form.buyer_name.data
        phone_number = form.phone_number.data
        password = form.password.data
        hashed_password = generate_password_hash(password)

        existing_user = User.query.filter_by(phone_number=phone_number).first()
        if existing_user:
            flash('Số điện thoại đã tồn tại. Vui lòng sử dụng số điện thoại khác.', 'error')
            return redirect(url_for('auth.register'))

        new_user = User(company_name=company_name, buyer_name=buyer_name, phone_number=phone_number, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Đăng ký thành công!')
        return redirect(url_for('home.home'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        password = form.password.data
        user = User.query.filter_by(phone_number=phone_number).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất.', 'success')
    return redirect(url_for('home.home'))
