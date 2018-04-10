# coding=utf-8
"""
GridfsBucket功能測試
"""

from flask import Flask
from pymongo import MongoClient
from gridfs import GridFSBucket
from gridfs import GridFS

uri = "mongodb://localhost:27017/" #個人測試用
client = MongoClient(uri)
db = client['test']
fs = GridFSBucket(db)
filename = "image1.jpg" #開啟檔案的名稱


def loadfile(fname):    
    try:        
        file = open(fname,'rb') #開啟fname        
        file_binary = file.read() #載入binary
        file.close()
        return file_binary
    except:
        print('file not found')
        return 0b0
    

def upload_file(fname,file_binary):
    #上傳
    grid_in = fs.open_upload_stream(fname,
                                    chunk_size_bytes=4,
                                    metadata = {"contentType": "text/plain"})    
    grid_in.write(file_binary)  #寫入binary
    grid_in.close() # uploaded on close
    print('upload done')

def upload_file_1(fname,file_binary):
    #上傳並寫入binary
    try:
        fs.upload_from_stream(fname,
                              file_binary,
                              chunk_size_bytes=4,
                              metadata = {"contentType": "text/plain"}) 
    except:
        print('err')    

    print('upload done')
    
def find(fname):
    i = 1 #計數器
    for grid_data in fs.find({"filename": fname},
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
    for grid_out in fs.find({"filename": fname},
                      no_cursor_timeout = True):
        contents_binary = grid_out.read()
        gname = grid_out.filename
        try:
            #開啟檔案，確認存在
            file = open(gname,'r')
        except:
            #直接創新檔
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
        

def delete(fname):
    for grid_data in fs.find({"filename": fname},
                             no_cursor_timeout = True):
        fs.delete(grid_data._id)
        print(str(grid_data.filename)+" has deleted")

file_data = loadfile(filename)
if not file_data == 0b0:
    upload_file_1(filename, file_data)
    find(filename)
    download(filename)