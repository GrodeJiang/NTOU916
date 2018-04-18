# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from base64 import b64encode
from pymongo import MongoClient
from gridfs import GridFS
from gridfs import GridFSBucket

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class DataForm(FlaskForm):
    filename = StringField('Enter the file name', validators=[Required()])
    submit = SubmitField('Submit')
    
def loadfile(fname):    
    try:        
        file = open(fname,'rb') #開啟fname        
        file_binary = file.read() #載入binary
        #binary --> base64   bytes --> str
        image = b64encode(file_binary).decode('ascii')
        file.close()
        return image
    except:
        print('file not found')
        return None
    
uri = "mongodb://localhost:27017/"#個人測試用
client = MongoClient(uri)
db = client['test']
gfs = GridFS(db , collection='gfs')
fs = GridFSBucket(db)

icon = loadfile('icon.png')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form1 = NameForm()
    if form1.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form1.name.data:
            flash('Looks like you have changed your name!')
            session['name'] = form1.name.data
            return redirect(url_for('index'))
    return render_template('index.html',
                           form = form1,
                           icon = icon,
                           name = session.get('name'))
    
@app.route('/image', methods=['GET', 'POST'])
def image():
    form1 = DataForm()
    image = []
    if form1.validate_on_submit():
        fname = session.get('imagename')
        session['imagename'] = form1.filename.data        
        return redirect(url_for('image')) 
    fname = session.get('filename')
    if fname is not None:
        i = 0 #計數器
        for grid_out in fs.find({"filename": fname},
                                 no_cursor_timeout = True):
            i+=1
            image.append(b64encode(grid_out.read()).decode('ascii'))
    return render_template('image.html',
                           form = form1,
                           icon = icon,
                           image = image)
    
@app.route('/data', methods=['GET', 'POST'])
def data():
    form1 = DataForm()
    data = []
    if form1.validate_on_submit():
        fname = session.get('filename')
        session['filename'] = form1.filename.data        
        return redirect(url_for('data'))    
    fname = session.get('imagename')
    if fname is not None:
        i = 0 #計數器
        for grid_out in fs.find({"filename": fname},
                                no_cursor_timeout = True):
            i+=1
            data.append((str(i)+":"+
                         "<br>  file name: "+str(grid_out.filename)+
                         "<br>  file id: "+str(grid_out._id)+
                         "<br>  upload time: "+str(grid_out.upload_date)+
                         "<br>  file length: "+str(grid_out.length)+"<br>"))
    return render_template('data.html',
                           form = form1,
                           data = data)

if __name__ == "__main__":
    app.run()
    
