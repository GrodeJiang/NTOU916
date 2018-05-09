# coding=utf-8
"""
Gridfs功能測試
"""

from flask import Flask
from pymongo import MongoClient
from gridfs import GridFSBucket
from gridfs import GridFS

uri = "mongodb://localhost:27017/" #個人測試用
client = MongoClient(uri)
db = client['test']
gfs = GridFS(db , collection='gfs')
filename = "uploadtest.jpg" #開啟檔案的名稱

def loadfile(fname):    
    try:
        file = open(fname,'rb') #開啟fname 
        file_binary = file.read() #載入binary
        file.close()
        return file_binary
    except:
        print('file not found')
        return 0b0

def upload(fname,data):
    try:
        f = gfs.new_file() #建新檔
        f.filename = fname #檔名
        f.write(data) #寫入binary
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

def find(fname):
    i = 1 #計數器
    for grid_data in gfs.find({"filename": fname},
                             no_cursor_timeout = True):
        filename = str(grid_data.filename)
        fileid = str(grid_data._id)
        uploadtime = str(grid_data.upload_date)
        print(str(i) + ":")
        print("file name: "+filename+"\nfile id: "+fileid
              +"\nupload time: "+uploadtime)
        i+=1

def download(fname):
    i = 1 #計數器
    for grid_out in gfs.find({"filename": fname},
                      no_cursor_timeout = True):
        contents_binary = grid_out.read()
        gname = grid_out.filename
        try:
            #開啟檔案，確認存在
            file = open(gname,'r')
        except:
            #不存在，直接創新檔
            file = open(gname,'wb')
        else:
            #已存在，另創新檔
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
