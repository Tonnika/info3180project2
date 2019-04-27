from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Email

class RegisterForm(FlaskForm):
    username=StringField('Username', validators=[InputRequired()])
    password=PasswordField('Password', validators=[InputRequired()])
    first_name=StringField('Firstname', validators=[InputRequired()])
    last_name=StringField('Lastname', validators=[InputRequired()])
    email=StringField('Email', validators=[InputRequired(), Email()])
    location=StringField('Location', validators=[InputRequired()])
    biography=StringField('Biography', validators=[InputRequired()])
    photo=FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg','png'],'Images Only')])
    
class LoginForm(FlaskForm):
    username=StringField('Username', validators=[InputRequired()])
    password=PasswordField('Password', validators=[InputRequired()])

class PostForm(FlaskForm):
    user_id=StringField("User ID",validators=[InputRequired()])
    photo=FileField('Photo', validators=[FileRequired()])
    caption=StringField('Caption',validators=[InputRequired()])