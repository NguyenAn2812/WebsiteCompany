from flask import Flask
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from app.models import db, User, PointHistory
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()

    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')

    db.init_app(app)

    csrf = CSRFProtect(app)
    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.product import product_bp
    app.register_blueprint(product_bp)

    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.routes.event import event_bp
    app.register_blueprint(event_bp)

    @app.cli.command('init-db')
    def init_db():
        with app.app_context():
            db.drop_all()  # Xóa tất cả các bảng hiện có
            db.create_all()  # Tạo lại các bảng

            admin_username = os.getenv('SUPER_ADMIN_USERNAME')
            admin_password = os.getenv('SUPER_ADMIN_PASSWORD')

            if admin_username and admin_password:
                admin_exists = User.query.filter_by(phone_number=admin_username).first()
                if not admin_exists:
                    admin = User(
                        company_name="Admin Company",
                        buyer_name="Super Admin",
                        phone_number=admin_username,
                        password_hash=generate_password_hash(admin_password),
                        role="superadmin"
                    )
                    db.session.add(admin)
                    db.session.commit()

            print('Initialized the database.')

    return app
