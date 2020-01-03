from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.fields.html5 import EmailField


class SignForm(FlaskForm) :

    email = EmailField('Enter Your Email', validators=[DataRequired(), Length(4, 128), Email()], render_kw={'placeholder': 'ادخل الايميل الالكترونى اللخاص بك', 'Autocomplete': 'off'})
    password = PasswordField('Enter Your Password', validators=[DataRequired(), Length(8, 128)], render_kw={'placeholder': 'ادخل كلمة السر الخاصة بك'})
    submit = SubmitField('تسجيل الدخول')

class RegisterForm(FlaskForm) :
    username = StringField('Enter Your Username', validators=[DataRequired(), Length(3, 128)], render_kw={'placeholder': 'ُEnter Your Username'})
    email = EmailField('Enter Your Email', validators=[DataRequired(), Length(4, 128), Email()], render_kw={'placeholder': 'Enter Your Email'})
    times = IntegerField('Enter Times', validators=[DataRequired()], render_kw={'placeholder': 'Enter Times'})
    password = PasswordField('Enter Your Password', validators=[DataRequired(), EqualTo('confirm', message="Password Must Be Matched"), Length(8, 128)], render_kw={'placeholder': 'Enter Your Password'})
    group_id = SelectField(u'Select Permission?', choices=[('', 'Select Permission'),('0', 'Normal User'), ('1', 'Admin')])
    confirm = PasswordField('Repeat Your Password',validators=[DataRequired()], render_kw={'placeholder': 'Repeat our Password'})
    submit = SubmitField('Submit')