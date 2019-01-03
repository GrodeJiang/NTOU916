# -*- coding: utf-8 -*-
from Database import Database
from FSBucket import FSBucket
from upload import upload_First, upload_Second, upload_Third
from Users import Users
import Forms as FM
from flask import Flask, render_template, session, redirect, url_for, flash, request, send_from_directory, send_file, abort
from flask_bootstrap import Bootstrap
from base64 import b64encode, b64decode
from werkzeug.utils import secure_filename
from bson import ObjectId
from flask_login import login_user, logout_user, login_required, LoginManager
import os
import io

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



UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'image')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    
icon = None
testuser = 'test'
usernamenow = 'test'

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bootstrap = Bootstrap(app)
login_manager.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader  
def user_loader(username):
    user = Users()
    if user.check(username):
        return user
    return   

@app.route('/', methods=['GET', 'POST'])
def index():
    form1 = FM.NameForm()
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

@app.route('/Image', methods=['GET', 'POST'])
def image():
    pid = 'test'
    username = testuser
    keys = []
    docids = []
    carouseldata = []
    userDB = Database(username)
    userdoc = userDB.Getdoc('name', username)
    for k in userdoc['list'].keys():
        keys.append(k)
    for d in userdoc['list'].values():
        docids.append(d)
    dataDB = Database(keys[0])
    dataFS = FSBucket(keys[0])
    datadoc = dataDB.Getdoc('_id', docids[0])
    imagedata = dataFS.Findbyid(datadoc['image'])
    if imagedata is not None:
        return send_file(
            io.BytesIO(imagedata),
            mimetype='image/jpeg')
    else:
        print("no image")
        abort(404)

@app.route('/Image/<username>/<ids>', methods=['GET', 'POST'])
def imageid(username, ids):
    dataDB = Database(username)
    dataFS = FSBucket(username)
    doc = dataDB.Getdoc("_id", ObjectId(ids))
    imagedata = dataFS.Findbyid(doc['image'])
    if imagedata is not None:
        return send_file(
            io.BytesIO(imagedata),
            mimetype='image/jpeg')
    else:
        print("no image")
        abort(404)

@app.route('/Carousel', methods=['GET', 'POST'])
def carousel():
    username = testuser
    keys = []
    dataids = []
    carouselid = []
    userDB = Database(username)
    #userFS = FSBucket(username)
    userdoc = userDB.Getdoc('name', username)
    try:        
        for k in userdoc['list'].keys():
            keys.append(k)
        for d in userdoc['list'].values():
            dataids.append(d)
        for i in range(0,len(keys)):
            carouselid.append(dataids[i])
    except:
        print('err')
        '''
        dataDB = Database(keys[i])
        dataFS = FSBucket(keys[i])
        datadoc = dataDB.Getdoc('_id', docids[i])
        imageid = datadoc['image']
        if imageid is not None:
            carouselid.append(imageid)
        '''
            
    return render_template('carouselid.html',
                           keys = keys,
                           carouselid = carouselid)
    
@app.route('/Carousel/<username>', methods=['GET', 'POST'])
def carousel_sec(username = None):
    if username is None:
        username = testuser
    #session['usernamenow'] = username
    keys = []
    carouselid = []
    dataDB = Database(username)
    datadoc = dataDB.Getdoc('name', username)
    dataids = []
    if datadoc != None:
        for k in datadoc['list'].keys():
            keys.append(k)
        for d in datadoc['list'].values():
            dataids.append(d)
        for i in range(0,len(keys)):
            carouselid.append(dataids[i])
    else:
        print('doc is not found')
        '''
        dataDB = Database(username)
        dataFS = FSBucket(username)
        datadoc = dataDB.Getdoc('_id', dataids[i])
        imageid = datadoc['image']
        if imageid is not None:
            carouselid.append(imageid)
        '''

    return render_template('carouselid.html',
                           username = username,
                           kinds = None,
                           keys = keys,
                           carouselid = carouselid)

@app.route('/Carousel/<username>/<kinds>', methods=['GET', 'POST'])
def carousel_third(username,kinds):
    if username is None:
        username = testuser
    carouselid = []
    dataDB = Database(username)
    datadoc = dataDB.Getdoc('name', kinds)
    Aform = FM.AlbumForm()
    if datadoc is not None:
        for ids in datadoc['list'].values():
            carouselid.append(ids)
        return render_template('albumid.html',
                               username = username,
                               kinds = kinds,
                               carouselid = carouselid,
                               Aform = Aform
                               )
    else:
        print("datadoc not found")
        return redirect(url_for('carousel_sec', username = username))
    #del dataDB,dataFS

@app.route('/Uploads', methods=['GET', 'POST'])
def upload_file():
    form1 = FM.UploadFirst()
    form2 = FM.UploadSecond()
    form3 = FM.UploadThird()
    if form1.submit1.data and form1.validate_on_submit():
        print('first')
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
            if(upload_First(form1, file)):
                flash('Upload done')
                return redirect(request.url)
            else:
                flash('Upload fail')
                return redirect(request.url)
        else:
            flash('File not allowed')
            return redirect(request.url)
    if form2.submit2.data and form2.validate_on_submit():
        print('sec')
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
            if(upload_Second(form2, file)):
                flash('Upload done')
                return redirect(request.url)
            else:
                flash('Upload fail')
                return redirect(request.url)
        else:
            flash('File not allowed')
            return redirect(request.url)
    if form3.submit3.data and form3.validate_on_submit():
        print('third')
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
            if(upload_Third(form3, file)):
                flash('Upload done')
                return redirect(request.url)
            else:
                flash('Upload fail')
                return redirect(request.url)
        else:
            flash('File not allowed')
            return redirect(request.url)
    return render_template('newupload.html',
                           form1 = form1,
                           form2 = form2,
                           form3 = form3)

@app.route('/Uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/Login', methods=['GET', 'POST'])
def login():    
    user = Users()
    form = FM.LoginForm()
    if form.validate_on_submit():
        logincheck = user.login(form.username.data,form.password.data)
        if logincheck is True:
            login_user(user)
            session['name'] = form.username.data
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html', form = form)
    
@app.route('/Logout')
@login_required
def logout():
    logout_user()
    session['name'] = None
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/Register', methods=['GET', 'POST'])
def register():
    user = Users()
    form = FM.RegistForm()
    if form.validate_on_submit():
        flag = user.register(form.username.data,form.password.data)
        if flag:
            flash('You can now login.')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)  
'''
if __name__ == "__main__":
    app.run()