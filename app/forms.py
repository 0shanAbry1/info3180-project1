from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField

from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired

from app import db
from models import UserProfile

class ProfileForm(FlaskForm):
    # Text fields >> StringField
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    username = StringField('User Name', validators=[InputRequired()])
    age = StringField('Age', validators=[InputRequired()])
    
    #Text field >> TextAreaField
    biography = TextAreaField('Biography', validators=[InputRequired()])
    
    #File upload field >> FileField
    image = FileField('Profile Picture', validators=[FileAllowed(['png','jpg','jpeg','gif'], 'Only an image file allowed')])
    
    #Select option >> SelectField
    gender = SelectField('Gender', choices=[('F','Female'),('M','Male'),('O','Other')])
    
    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        
    def validate(self):
        """Uniqueness of the username entered"""
        if not FlaskForm.validate(self):
            return False
            
        username_data = UserProfile.query.filter_by(username=self.username.data).first()
        
        if(username_data):
            # Not unique if the username was found in the database
            self.username.errors.append("Username entered already exists")
            return False
        else:
            return True