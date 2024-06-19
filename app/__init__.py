from flask import Flask
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from app.models import db, User

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    db.init_app(app)
    csrf = CSRFProtect(app)

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

    @app.cli.command('init-db')
    def init_db():
        db.create_all()
        print('Initialized the database.')

    return app
