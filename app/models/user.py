from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    buyer_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    points = db.Column(db.Integer, default=0)
    role = db.Column(db.String(50), default='user')  # Thêm thuộc tính role
    orders = db.relationship('Order', backref='user', lazy=True)
    promotion_codes = db.relationship('PromotionCode', backref='user', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    details = db.Column(db.String(255), nullable=False)

class PromotionCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    code = db.Column(db.String(50), unique=True, nullable=False)
