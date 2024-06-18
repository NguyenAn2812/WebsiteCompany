from flask import Blueprint

bp = Blueprint('product', __name__)

@bp.route('/products')
def products():
    # Thực hiện hiển thị danh sách sản phẩm
    return 'List of products'
