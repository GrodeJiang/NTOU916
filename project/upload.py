# -*- coding: utf-8 -*-
import os
from Database import Database
from FSBucket import FSBucket
from werkzeug.utils import secure_filename

mainname = 'test'
mainDB = Database(mainname)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'image')

def upload_First(form, file):
    username = form.username.data
    dataDB = Database(username)
    dataFS = FSBucket(username)
    mdoc = mainDB.Getdoc('name', mainname)
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    fileid = dataFS.Upload(os.path.join(UPLOAD_FOLDER,filename), filename)
    doc =  dataDB.Getdoc('name', username)
    if doc is None:
        docid = dataDB.Upload(username, fileid, {})
    else:
        doc.imageid = fileid
        if (dataDB.Modify('name', username, doc) == False):
            return False
    mdoc['list'][username] = docid
    print('ok')
    if (mainDB.Modify('name', mainname, mdoc)):
        return True
    return False

def upload_Second(form, file):
    username = form.username.data
    dataDB = Database(username)
    dataFS = FSBucket(username)
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    fileid = dataFS.Upload(os.path.join(UPLOAD_FOLDER,filename), filename)
    userdoc = dataDB.Getdoc("name", username) 
    if userdoc is None:
        print('username not found')
        return False
    docid = dataDB.Upload(form.kinds.data, fileid, {})
    userdoc['list'][form.kinds.data] = docid
    dataDB.Modify("_id", userdoc['_id'], userdoc)
    return True

def upload_Third(form, file):
    username = form.username.data
    dataDB = Database(username)
    dataFS = FSBucket(username)
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    fileid = dataFS.Upload(os.path.join(UPLOAD_FOLDER,filename), filename)
    kindsdoc = dataDB.Getdoc("name", form.kinds.data)
    if kindsdoc is None:
        print('kinds not found')
        return False
    fname = form.kinds.data + "_" + form.itemname.data
    docid = dataDB.Upload(fname,fileid, None)
    kindsdoc['list'][fname] = docid
    dataDB.Modify("_id", kindsdoc['_id'], kindsdoc)
    return True