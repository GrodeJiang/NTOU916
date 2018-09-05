# -*- coding: utf-8 -*-
from flask.ext.wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, EqualTo

class NameForm(FlaskForm):
    name = StringField('What is your name?', [Required()])
    submit = SubmitField('Submit')
    
class DataForm(FlaskForm):
    filename = StringField('Enter the file name', [Required()])
    submit = SubmitField('Submit')
    
class UploadForm(FlaskForm):
    username = StringField('Enter the user name', validators=[Required()])
    kinds = StringField('Enter the kinds name', [Required()])
    itemname = StringField('Enter the item name')
    file = FileField('Choose image', [FileRequired()])
    submit = SubmitField('Submit')
    
class LoginForm(FlaskForm):
    username = StringField('Enter the username', [Required()])
    password = PasswordField('Enter the password', [Required()])
    submit = SubmitField('Log In')
    
class RegistForm(FlaskForm):
    username = StringField('Enter the username', [Required()])
    password = PasswordField('Enter the password', [Required()])
    comfirmpw = PasswordField('Repeat Password', [Required(), EqualTo('password', message='please check your password')])
    submit = SubmitField('Regist')