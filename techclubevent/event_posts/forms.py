from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class EventPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Post')

class EventRegistrationForm(FlaskForm):
    event = SelectField(
        'Choose Event',
        coerce=int,
        validators=[DataRequired()]
    )
    submit = SubmitField('Register for Event')


