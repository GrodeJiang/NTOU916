# -*- coding: utf-8 -*-
from Database import Database
from FSBucket import FSBucket
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from base64 import b64encode

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
        
icon = None
testuser = 'test'
usernamenow = 'test'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

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
        carouseldata.append(b64encode(dataFS.Findbyid(imageid)).decode('ascii'))
    del dataDB,dataFS
            
    return render_template('carousel.html', 
                           keys = keys,
                           carouseldata = carouseldata)
    
@app.route('/Carousel/<username>', methods=['GET', 'POST'])
def Carousel_final(username = None):
    if username is None:
        username = testuser
    keys = []
    carouseldata = []
    dataDB = Database(username)
    dataFS = FSBucket(username)
    #userFS = FSBucket(username)
    datadoc = dataDB.Getdoc('name', username)
    for k in datadoc['list'].keys():
        keys.append(k)
    for ids in datadoc['list'].values():
        carouseldata.append(b64encode(dataFS.Findbyid(ids)).decode('ascii'))
    #del dataDB,dataFS
            
    return render_template('carousel.html', 
                           keys = keys,
                           carouseldata = carouseldata)


    
if __name__ == "__main__":
    app.run()