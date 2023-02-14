from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import Form, StringField, SelectField, validators, ValidationError, PasswordField, SubmitField, \
    BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired


def nric_check(form, field):
    if field.data[0].isalpha() is False or field.data[1:8].isnumeric() is False or field.data[-1].isalpha() is False:
        raise ValidationError('NRIC is invalid')
    if len(field.data) != 9:
        raise ValidationError('NRIC is invalid')
    str = field.data.upper()
    weight = 0
    weight += int(field.data[1]) * 2
    weight += int(field.data[2]) * 7
    weight += int(field.data[3]) * 6
    weight += int(field.data[4]) * 5
    weight += int(field.data[5]) * 4
    weight += int(field.data[6]) * 3
    weight += int(field.data[7]) * 2

    if str[0] == "T" or "G":
        weight += 4

    temp = weight % 11

    st = ["J","Z","I","H","G","F","E","D","C","B","A"]
    fg = ["X","W","U","T","R","Q","P","N","M","L","K"]
    alpha = ""
    if str[0] == "S" or "T":
        alpha = st[temp]
    elif str[0] == "F" or "T":
        alpha = fg[temp]

    if str[8] != alpha:
        raise ValidationError('NRIC is invalid')


class CreateEmployeeForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    position = StringField('Position', [validators.DataRequired(), validators.Length(min=1, max=150)])
    NRIC = StringField('NRIC', [validators.Length(min=9, max=9), validators.DataRequired(), nric_check])


def password_num(form, field):
    if any(i.isnumeric() for i in field.data) is False:
        raise ValidationError("Password must have at least one number")


def password_upper(form, field):
    if any(i.isupper() for i in field.data) is False:
        raise ValidationError("Password must have at least one uppercase character")


def password_lower(form, field):
    if any(i.islower() for i in field.data) is False:
        raise ValidationError("Password must have at least one lowercase character")


class RegisterAccountForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1, max=20), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired(), validators.Email("A valid email address is required")])
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired(), password_upper,
                                          password_lower, password_num])
    confirm_password = PasswordField('Confirm Password',
                                     [validators.Length(min=10, max=150), validators.DataRequired(),
                                      validators.EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')


class Login(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember Me', validators=[validators.DataRequired()])
    submit = SubmitField('Login')


class InventoryEdit(FlaskForm):
    image = FileField('Product Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only.')])
    name = StringField('Product Name', [validators.DataRequired()])
    price = StringField('Price', [validators.DataRequired()])
    quantity = IntegerField('Quantity', [validators.DataRequired()])


class CreditCardForm(Form):
    cardholder = StringField('Name (on card)', [validators.Length(min=1, max=150), validators.DataRequired()])
    cardnumber = IntegerField('Card Number', [validators.NumberRange(min=1000000000000000, max=9999999999999999), validators.DataRequired()])
    exp_month = IntegerField('Month in (MM)', [validators.NumberRange(min=1, max=12), validators.DataRequired()])
    exp_year = IntegerField('Year in (YYYY)', [validators.NumberRange(min=2023, max=2100), validators.DataRequired()])
    verification = IntegerField('CVV', [validators.NumberRange(min=100, max=999), validators.DataRequired()])


class GymLocationForm(Form):
    locationAddress = StringField('Location Name', validators=[DataRequired()])
    lat = FloatField('Latitude', validators=[DataRequired()])
    lng = FloatField('Longitude', validators=[DataRequired()])
