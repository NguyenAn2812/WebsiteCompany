import pandas as pd
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, PromotionCode
import os

event_bp = Blueprint('event', __name__)

@event_bp.route('/event', methods=['GET', 'POST'])
@login_required
def event():
    if request.method == 'POST':
        code = request.form.get('promotion_code')
        if not code:
            flash('Please enter a promotion code.', 'danger')
            return redirect(url_for('event.event'))

        # Đường dẫn tới file CSV lưu trữ mã khuyến mãi
        csv_file = os.path.join(os.path.dirname(__file__), '../database/promotioncodelist.csv')

        # Đọc dữ liệu CSV
        df = pd.read_csv(csv_file)

        # Kiểm tra mã khuyến mãi
        if code in df['code'].values:
            code_index = df[df['code'] == code].index[0]
            if df.at[code_index, 'used']:
                flash('This promotion code has already been used.', 'danger')
            else:
                df.at[code_index, 'used'] = True
                df.to_csv(csv_file, index=False)
                current_user.points += 10  # Ví dụ: Cộng 10 điểm cho người dùng
                db.session.commit()
                flash('Promotion code applied successfully!', 'success')
        else:
            flash('Invalid promotion code.', 'danger')

    return render_template('event.html')
