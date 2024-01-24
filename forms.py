from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username:',
                           validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password:',
                           validators=[InputRequired(), Length(min=1, max=55)])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('Username:',
                           validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password:',
                           validators=[InputRequired(), Length(min=1, max=55)])
    email = StringField('Email:',
                        validators=[InputRequired(), Length(min=1, max=50)])
    first_name = StringField('First Name:',
                             validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField('Last Name:',
                            validators=[InputRequired(), Length(min=1, max=30)])
    submit = SubmitField('Submit')

class FeedbackForm(FlaskForm):
    title = StringField('Title:',
                        validators=[InputRequired(), Length(min=1, max=100)])
    content = TextAreaField('Content:',
                            validators=[InputRequired()])
    
class DeleteForm(FlaskForm):
     """Delete form -- this form is intentionally blank."""