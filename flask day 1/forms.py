from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     DecimalField,
                    SelectField,
                    IntegerField,
                    SubmitField)
from wtforms.validators import DataRequired,Length, Regexp

class BioDataForm(FlaskForm):
    hometown = StringField(label='Home Town',validators=[DataRequired()]) 
    contact = StringField(label='Phone', validators=[DataRequired(message='Value Required For Phone'), Regexp(r'^\d+$', message='contact should be a number'), Length(min=10, max=13, message='Number should be between 10 and 13 digits')])   
    submit = SubmitField(label='Update Bio data')
