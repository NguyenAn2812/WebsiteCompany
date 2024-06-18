from flask import Blueprint, render_template, request

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Mã hóa mật khẩu và lưu vào CSDL
        # Chuyển hướng đến trang đăng nhập hoặc dashboard
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Kiểm tra thông tin đăng nhập
        # Chuyển hướng người dùng đến dashboard
    return render_template('login.html')

