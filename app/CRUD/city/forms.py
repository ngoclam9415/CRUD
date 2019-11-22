from flask_wtf import Form
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email


class RegisterForm(Form):
    email = EmailField('email', validators=[DataRequired(), Email(
        message=None), Length(min=6, max=40)]
    )
    password = PasswordField('password',
                             validators=[DataRequired(), Length(min=3, max=25)]
                             )
