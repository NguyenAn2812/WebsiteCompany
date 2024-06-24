from flask import Blueprint, render_template

product_bp = Blueprint('product', __name__)

@product_bp.route('/products')
def products():
    return render_template('products.html')
