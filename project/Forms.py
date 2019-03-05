# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import Required, EqualTo, length, Regexp

class NameForm(FlaskForm):
    name = StringField('What is your name?', [Required()])
    submit = SubmitField('Submit')
    
class DataForm(FlaskForm):
    filename = StringField('Enter the file name', [Required()])
    submit = SubmitField('Submit')
    
class UploadFirst(FlaskForm):
    username = StringField('Enter the name of the first stage', validators=[Required(), 
		        Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                'usernames must have only letters, '
                'numbers, dots or underscores')])
    file = FileField('Choose image', [FileRequired()])
    submit1 = SubmitField('Submit')

class UploadSecond(FlaskForm):
    username = StringField('Enter the name of the first stage', validators=[Required(), 
		        Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                'usernames must have only letters, '
                'numbers, dots or underscores')])
    kinds = StringField('Enter the name of the second stage', validators=[Required(),
                Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                'kinds must have only letters, '
                'numbers, dots or underscores')])
    file = FileField('Choose image', [FileRequired()])
    submit2 = SubmitField('Submit')

class UploadThird(FlaskForm):
    username = StringField('Enter the name of the first stage', validators=[Required(), 
		        Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                'usernames must have only letters, '
                'numbers, dots or underscores')])
    kinds = StringField('Enter the name of the second stage', validators=[Required(),
                Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                'kinds must have only letters, '
                'numbers, dots or underscores')])
    itemname = StringField('Enter the name of the third stage', validators=[Required(),
                Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                'itemname must have only letters, '
                'numbers, dots or underscores')])
    price = IntegerField('Item price', validators=[Required()])
    file = FileField('Choose image', [FileRequired()])
    submit3 = SubmitField('Submit')
    
class LoginForm(FlaskForm):
    username = StringField('Enter the username', [Required()])
    password = PasswordField('Enter the password', [Required()])
    submit = SubmitField('Log In')
    
class RegistForm(FlaskForm):
    username = StringField('Enter the username', validators=[
                Required(), length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                'Usernames must have only letters, '
                'numbers, dots or underscores')])
    password = PasswordField('Enter the password', [Required()])
    comfirmpw = PasswordField('Repeat Password', [Required(), EqualTo('password', message='please check your password')])
    submit = SubmitField('Regist')
class AlbumForm(FlaskForm):
    imageid = ""
    addcar = SubmitField('add car')