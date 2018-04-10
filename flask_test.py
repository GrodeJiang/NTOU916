# -*- coding: utf-8 -*-
"""
開啟圖片並讀取binary後
轉回圖片並傳至綱頁
"""

from flask import Flask
from flask import send_file
import io

filename = "image.jpg" #開啟檔案的名稱

def loadfile(fname):    
    try:        
        file = open(fname,'rb') #開啟fname        
        file_binary = file.read() #載入binary
        file.close()
        return file_binary
    except:
        #print('file not found')
        return 0b0
    
image_data = loadfile(filename)

app = Flask(__name__)

@app.route("/")
def image():
    #將圖片BINARY轉成圖片後回傳
    if not image_data == 0b0:
        return send_file(io.BytesIO(image_data),
                         attachment_filename='test.jpg',
                         mimetype='image/jpg')
    else:
        #圖片不存在時觸發
        return "file not found"

if __name__ == "__main__":
    app.run()
    
