from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    phone_number = StringField('Số điện thoại', validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')

class RegisterForm(FlaskForm):
    company_name = StringField('Tên công ty', validators=[DataRequired(), Length(max=100)])
    buyer_name = StringField('Tên người mua', validators=[DataRequired(), Length(max=100)])
    phone_number = StringField('Số điện thoại', validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đăng ký')
