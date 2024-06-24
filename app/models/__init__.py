from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .order import Order
from .promotion_code import PromotionCode
from .point_history import PointHistory
