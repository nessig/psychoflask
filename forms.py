from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(Form):
    username = TextField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = TextField(
        'email',
        # validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
        validators=[DataRequired(), Email(message=None)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired()]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )

class EditForm(Form):
    text = TextAreaField('About me', validators=[DataRequired()])
