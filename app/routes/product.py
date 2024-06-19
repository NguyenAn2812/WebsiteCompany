from flask import Blueprint

product_bp = Blueprint('product', __name__)

@product_bp.route('/products')
def products():
    return 'List of products'
