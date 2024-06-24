import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, PromotionCode, PointHistory
from app.forms import PromoCodeForm

# Configure logging
logging.basicConfig(level=logging.INFO)
event_bp = Blueprint('event', __name__)

@event_bp.route('/event', methods=['GET', 'POST'])
@login_required
def event():
    form = PromoCodeForm()
    if form.validate_on_submit():
        logging.info("Received POST request")
        code = form.code.data
        logging.info(f"Promotion code received: {code}")

        if not code:
            logging.error("No promotion code provided")
            flash('Please enter a promotion code.', 'danger')
            return redirect(url_for('event.event'))

        # Kiểm tra mã khuyến mãi trong cơ sở dữ liệu
        promo_code = PromotionCode.query.filter_by(code=code).first()
        if promo_code:
            logging.info(f"Promotion code found: {promo_code.code}")

            if promo_code.used:
                logging.warning("Promotion code has already been used")
                flash('This promotion code has already been used.', 'danger')
            else:
                promo_code.used = True
                db.session.commit()

                # Cộng 5 điểm cho người dùng
                current_user.points += 5
                db.session.commit()

                # Ghi lại lịch sử
                point_history = PointHistory(
                    user_id=current_user.id,
                    change=5,
                    reason=f'Used promotion code: {code}',
                    admin_id=None  # Không có admin
                )
                db.session.add(point_history)
                db.session.commit()

                logging.info(f"Promotion code applied successfully. New points: {current_user.points}")
                flash('Promotion code applied successfully! You earned 5 points.', 'success')
        else:
            logging.warning("Invalid promotion code")
            flash('Invalid promotion code.', 'danger')

    # Lấy lịch sử điểm của người dùng
    point_history = PointHistory.query.filter_by(user_id=current_user.id).all()

    return render_template('event.html', form=form, current_user=current_user, point_history=point_history)
