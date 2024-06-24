from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    buyer_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    points = db.Column(db.Integer, default=0)
    orders = db.relationship('Order', backref='user', lazy=True)
    promotion_codes = db.relationship('PromotionCode', backref='user', lazy=True)
    role = db.Column(db.String(20), default='user')  # role: user, hr_admin, customer_admin

