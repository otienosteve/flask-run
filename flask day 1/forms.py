from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     DecimalField,
                    SelectField,
                    IntegerField,
                    SubmitField, PasswordField)
from wtforms.validators import DataRequired,Length, Regexp, Email, EqualTo

class BioDataForm(FlaskForm):
    hometown = StringField(label='Home Town',validators=[DataRequired()]) 
    contact = StringField(label='Phone', validators=[DataRequired(message='Value Required For Phone'), Regexp(r'^\d+$', message='contact should be a number'), Length(min=10, max=13, message='Number should be between 10 and 13 digits')])   
    submit = SubmitField(label='Update Bio data')

class RegisterForm(FlaskForm):
    email = StringField(label='Email',validators=[DataRequired(),Email()])
    password = PasswordField(label='Password',validators=[DataRequired(),Length(min=8,max=28)])
    confirm_password = PasswordField(label='Confirm Password',validators=[DataRequired(),Length(min=8,max=28), EqualTo('password')])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = StringField(label='Email',validators=[DataRequired(),Email()])
    password = PasswordField(label='Password',validators=[DataRequired(),Length(min=8,max=28)])
    submit = SubmitField(label='Login')