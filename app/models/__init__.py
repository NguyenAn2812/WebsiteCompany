from flask import Flask
from .routes.auth import bp as auth_bp  # Đảm bảo đã nhập đúng tên Blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    from .models import db
    db.init_app(app)

    app.register_blueprint(auth_bp)

    return app
