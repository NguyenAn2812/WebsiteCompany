from flask import Blueprint, render_template
from flask_login import login_required, current_user

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')
