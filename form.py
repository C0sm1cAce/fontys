from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Email

class CheckoutForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
    checkin = DateField('Check-in Date', format='%Y-%m-%d', validators=[DataRequired()])
    checkout = DateField('Check-out Date', format='%Y-%m-%d', validators=[DataRequired()])
    cardnumber = StringField('Credit Card Number', validators=[DataRequired()])
    expiration = DateField('Expiration Date', format='%Y-%m-%d', validators=[DataRequired()])
    cvv = IntegerField('CVV', validators=[DataRequired()])
