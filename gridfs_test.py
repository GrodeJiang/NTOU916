# coding=utf-8
from flask import Flask
from pymongo import MongoClient
from gridfs import GridFSBucket
from gridfs import GridFS

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client['test']
gfs = GridFS(db , collection='gfs')
filename = "uploadtest.jpg"
def loadfile(fname):    
    try:
        file = open(fname,'rb')
        file_binary = file.read()
        file.close()
        return file_binary
    except:
        print('file not found')
        return 0b0

def upload(fname,data):
    try:
        f = gfs.new_file()
        f.filename = fname
        f.write(data)
        print('done')
        f.close()
    except:
        print('err')

def checkfile(fname):
   check = gfs.exists({"filename": fname})
   if  check == True:
       print('file exists')
   else:
       print('file not exists')

def download(fname):
    i = 1
    for grid_out in gfs.find({"filename": fname},
                      no_cursor_timeout = True):
        #grid_out = fs.open_download_stream_by_name(fname)
        contents_binary = grid_out.read()
        gname = grid_out.filename
        try:
            """開啟檔案，確認存在"""
            file = open(gname,'r')
        except:
            """直接創新檔"""
            file = open(gname,'wb')
        else:
            """已存在，另創新檔"""
            file.close()
            print("file already exist,so creat new file name:" + str(i) + "_" + gname)
            file = open(str(i) + "_" + gname,'wb')
        file.write(contents_binary)
        file.close()
        i+=1
    print("download done")
    

filedata = loadfile(filename)
upload(filename,filedata)
checkfile(filename)
download(filename)
