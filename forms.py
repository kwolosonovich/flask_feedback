from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, URL, Email, Optional
from flask_wtf import FlaskForm

# validators
required = InputRequired()
email_validator = Email(message='Please provide a valid email address')
len_20 = Length(max=20)
len_30 = Length(max=30)
len_50 = Length(max=50)
url_validator = URL(message='Please provide valid URL')
optional = Optional(strip_whitespace=True)


class RegisterForm(FlaskForm):
    '''New user registration form.'''

    #form input fields
    username = StringField("Username", validators=[required, len_20])
    password = PasswordField("Password", validators=[required])
    email = StringField("Email", validators=[required, email_validator])
    first_name = StringField("First Name", validators=[required, len_30])
    last_name = StringField("Last Name", validators=[required, len_30])
    profile_photo = StringField('Profile Photo', validator=[optional, url_validator])

