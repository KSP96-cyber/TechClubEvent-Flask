from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    event = SelectField('Event', choices=[], validators=[DataRequired()])
    submit = SubmitField('Register')
