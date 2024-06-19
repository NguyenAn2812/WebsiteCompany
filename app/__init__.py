from flask import Flask
from flask_wtf import CSRFProtect
from app.models import db

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Thay thế bằng khóa bí mật của bạn

    db.init_app(app)
    csrf = CSRFProtect(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.product import product_bp
    app.register_blueprint(product_bp)

    @app.cli.command('init-db')
    def init_db():
        db.create_all()
        print('Initialized the database.')

    return app
