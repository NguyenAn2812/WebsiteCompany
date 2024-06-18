from flask import Flask
from app.routes.auth import bp as auth_bp  
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    from app.models import db
    db.init_app(app)

    app.register_blueprint(auth_bp)

    return app
