# coding=utf-8
"""
從Mongo資料庫取圖片binary後
轉回圖片並傳至綱頁
"""

from flask import Flask
from pymongo import MongoClient
from gridfs import GridFSBucket
from flask import send_file
import io

uri = "mongodb://localhost:27017/"#個人測試用
client = MongoClient(uri)
db = client['test']
fs = GridFSBucket(db)
filename = "uploadtest.jpg" #開啟檔案的名稱

def find(fname):
    #向資料庫要圖片BINARY
    for grid_out in fs.find({"filename": fname},
                            no_cursor_timeout = True):
        return grid_out.read()
    #不存在時
    else:
        return 0b0


image_data = find(filename)

app = Flask(__name__)

@app.route("/")
def image():
    #將圖片BINARY轉成圖片後回傳至網站
    if not image_data == 0b0:
        return send_file(io.BytesIO(image_data),
                         attachment_filename='test.jpg',
                         mimetype='image/jpg')
    else:
        #圖片不存在時觸發
        return "file not found"

if __name__ == "__main__":
    app.run()

