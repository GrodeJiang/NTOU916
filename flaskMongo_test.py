# coding=utf-8
"""
從Mongo資料庫取圖片binary後
轉回圖片並傳至綱頁
"""

import io
from flask import Flask
from pymongo import MongoClient
from gridfs import GridFS
from gridfs import GridFSBucket
from flask import send_file
from bson import ObjectId

uri = "mongodb://localhost:27017/"#個人測試用
client = MongoClient(uri)
db = client['test']
gfs = GridFS(db , collection='gfs')
fs = GridFSBucket(db)


app = Flask(__name__)

@app.route("/")
def home():
    return ("查詢資料：在位址後加入\"/data/檔名\"<br/>"+
            "開啟圖片：在位址後加入\"/image/id\"<br/>")

@app.route("/data/<string:fname>")
def data(fname):
    i = 0 #計數器
    data = ""
    for grid_out in fs.find({"filename": fname},
                             no_cursor_timeout = True):
        i+=1
        data += (str(i)+":"+
                 "<br/>file name: "+str(grid_out.filename)+
                 "<br/>file id: "+str(grid_out._id)+
                 "<br/>upload time: "+str(grid_out.upload_date)+
                 "<br/>file length: "+str(grid_out.length)+"<br/>")
    else:
        return data
    #不存在時觸發
    return "file not found"
    

@app.route("/image/<string:file_id>")
def image(file_id):
    #file_id (string)-->(ObjectId) 才能跑
    grid_out = fs.open_download_stream(ObjectId(file_id))
    return send_file(io.BytesIO(grid_out.read()),
                     attachment_filename='test.jpg',
                     mimetype='image/jpg')

"""未完成       
@app.route("/imagebyname/<string:fname>")
def image_name(fname):
    i = 0 #計數器
    for grid_out in fs.find({"filename": fname},
                             no_cursor_timeout = True):
        i+=1
    else:
        return send_file(io.BytesIO(grid_out.read()),
                     attachment_filename='test.jpg',
                     mimetype='image/jpg')
    #不存在時觸發
    return "file not found"
"""    

if __name__ == "__main__":
    app.run()

