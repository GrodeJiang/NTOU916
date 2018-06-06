# -*- coding: utf-8 -*-
from Database import Database
from FSBucket import FSBucket
from flask import Flask, render_template, session, redirect, url_for, flash, request, send_from_directory
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from base64 import b64encode
from werkzeug.utils import secure_filename
from bson import ObjectId
import os

'''
CircleFS = FSBucket('Circle')
cirid = CircleFS.Upload('circle.jpg')
blackid = CircleFS.Upload('cirblack.jpg')
blueid = CircleFS.Upload('cirblue.jpg')
redid = CircleFS.Upload('cirred.jpg')
CirDB = Database('Circle')
info = ['black', 'blue', 'red']
data = [blackid, blueid, redid]
listdata = CirDB.Makelist(info,data)
DBid = CirDB.Upload('Circle', cirid, listdata)
'''

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
    
class DataForm(FlaskForm):
    filename = StringField('Enter the file name', validators=[Required()])
    submit = SubmitField('Submit')
    
class UploadForm(FlaskForm):
    username = StringField('Enter the user name', validators=[Required()])
    kinds = StringField('Enter the kinds name', validators=[Required()])
    itemname = StringField('Enter the item name')
    file = FileField('Choose image', validators=[FileRequired()])
    submit = SubmitField('Submit')

UPLOAD_FOLDER = 'D:\python\picture'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    
icon = None
testuser = 'test'
usernamenow = 'test'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bootstrap = Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    form1 = NameForm()
    if form1.validate_on_submit():
        old_name = session.get('name')        
        session['name'] = form1.name.data
        if old_name is not None and old_name != form1.name.data:
            flash('Looks like you have changed your name!')
            return redirect(url_for('index'))
    return render_template('index.html',
                           form = form1,
                           icon = icon,
                           name = session.get('name'))
    
@app.route('/Carousel', methods=['GET', 'POST'])
def Carousel():
    username = testuser
    keys = []
    docids = []
    carouseldata = []
    userDB = Database(username)
    #userFS = FSBucket(username)
    userdoc = userDB.Getdoc('name', username)
    for k in userdoc['list'].keys():
        keys.append(k)
    for d in userdoc['list'].values():
        docids.append(d)
    for i in range(0,len(keys)):
        dataDB = Database(keys[i])
        dataFS = FSBucket(keys[i])
        datadoc = dataDB.Getdoc('_id', docids[i])
        imageid = datadoc['image']
        imagedata = dataFS.Findbyid(imageid)
        if imagedata is not None:
            carouseldata.append(b64encode(imagedata).decode('ascii'))
    del dataDB,dataFS
            
    return render_template('carousel.html', 
                           keys = keys,
                           carouseldata = carouseldata)
    
@app.route('/Carousel/<username>', methods=['GET', 'POST'])
def carousel_sec(username = None):
    if username is None:
        username = testuser
    #session['usernamenow'] = username
    keys = []
    carouseldata = []
    dataDB = Database(username)
    dataFS = FSBucket(username)
    #userFS = FSBucket(username)
    datadoc = dataDB.Getdoc('name', username)
    dataids = []
    '''
    for k in datadoc['list'].keys():
        keys.append(None)
    '''
    for k in datadoc['list'].keys():
        keys.append(k)
    for d in datadoc['list'].values():
        dataids.append(d)
    for i in range(0,len(keys)):
        dataDB = Database(username)
        dataFS = FSBucket(username)
        datadoc = dataDB.Getdoc('_id', dataids[i])
        imageid = datadoc['image']
        imagedata = dataFS.Findbyid(imageid)
        if imagedata is not None:
            carouseldata.append(b64encode(imagedata).decode('ascii'))
    del dataDB,dataFS

    return render_template('carousel.html',
                           username = username,
                           kinds = None,
                           keys = keys,
                           carouseldata = carouseldata)

@app.route('/Carousel/<username>/<kinds>', methods=['GET', 'POST'])
def carousel_third(username,kinds):
    if username is None:
        username = testuser
    keys = None
    carouseldata = []
    dataDB = Database(username)
    dataFS = FSBucket(username)
    #userFS = FSBucket(username)
    datadoc = dataDB.Getdoc('name', kinds)
    '''
    for k in datadoc['list'].keys():
        keys.append(None)
    '''
    if datadoc is not None:
        for ids in datadoc['list'].values():
            doc = dataDB.Getdoc('_id', ids)
            imagedata = dataFS.Findbyid(doc['image'])
            if imagedata is not None:
                carouseldata.append(b64encode(imagedata).decode('ascii'))
        return render_template('carousel.html',
                               username = username,
                               kinds = kinds,
                               keys = keys,
                               carouseldata = carouseldata)
    else:
        print("datadoc not found")
        return redirect(url_for('carousel_sec', username = username))
    #del dataDB,dataFS

    


@app.route('/Uploads', methods=['GET', 'POST'])

def upload_file():
    existflag = True
    form1 = UploadForm()
    username = testuser
    if form1.validate_on_submit():
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            username = form1.username.data
            dataDB = Database(username)
            dataFS = FSBucket(username)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileid = dataFS.Upload(os.path.join(app.config['UPLOAD_FOLDER'],filename), filename)
            #upload item
            if form1.itemname.data is not None:
                kindsdoc = dataDB.Getdoc("name", form1.kinds.data)
                if kindsdoc is not None:
                    docid = dataDB.Upload(form1.kinds.data + "_" + form1.itemname.data,
                                          fileid, None)
                    kindslist = kindsdoc['list']
                    if kindslist is None:
                        kindslist = {}
                    kindslist[form1.kinds.data + "_" + form1.itemname.data] = docid
                    kindsdoc['list'] = kindslist
                    dataDB.Modify("_id", kindsdoc['_id'], kindsdoc)
                    existflag = False
                else:
                    print("get kinds fail")
            #upload kinds
            else:
                userdoc = dataDB.Getdoc("name", form1.username.data)
                if userdoc is not None:
                    docid = dataDB.Upload(form1.kinds.data,
                                          fileid, None)
                    userlist = userdoc['list']
                    userlist[form1.kinds.data] = docid
                    userdoc['list'] = userlist
                    dataDB.Modify("_id", userdoc['_id'], userdoc)
                    existflag = False
            if existflag is True:
                flash('Kinds or item does not exist')
                return redirect(request.url)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('uptest.html',
                           form = form1)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


    
if __name__ == "__main__":
    app.run()