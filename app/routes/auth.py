from flask import Blueprint

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Thực hiện chức năng đăng nhập
    return 'Login page'

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Thực hiện chức năng đăng ký
    return 'Register page'
