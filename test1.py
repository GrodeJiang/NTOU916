# coding=utf-8
from flask import Flask
from pymongo import MongoClient
from gridfs import GridFSBucket
from gridfs import GridFS

"""
沒問題，但等後面處理完
app = Flask(__name__)
@app.route('/')
"""
def root():    
	return "Hello World!!"

#uri = "mongodb://BB1:a12151456@172.25.3.41/?authSource=test"
uri = "mongodb://localhost:27017/" #個人測試用

client = MongoClient(uri)
db = client['test']
gfs = GridFS(db , collection='gfs')

#存進id作分類
if gfs.exists({"_id": "lisa.txt"}):
    #lisa.txt存在
    print("file exists")
    #讀取lisa.txt內容
    for grid_out in gfs.find({"filename": "lisa.txt"},
                            no_cursor_timeout=True):
        data = grid_out.read()  #將內容存進data
else:
    print('file NOT exists')


#將檔案上傳至stream?
#my_db = MongoClient().test  前面已宣告
fsbucket = GridFSBucket(db)
grid_in = fsbucket.open_upload_stream( "test_file",
                                chunk_size_bytes=4,
                                metadata={"contentType": "text/plain"}) 
grid_in.write('data I want to store!'.encode("UTF-8")) 
grid_in.close() # uploaded on close


   

#將檔案從db下載   
""" 
前面已宣告
my_db = MongoClient().test 
fsb = GridFSBucket(my_db) 
""" 
# get _id of file to read.  上傳並取得id
file_id = fsbucket.upload_from_stream("test_file", 'data I want to store!'.encode('utf-8'))
print('done')
grid_out = fsbucket.open_download_stream(file_id)
contents = grid_out.read() #讀取內容
print(contents) #輸出內容
"""
結果: b'data I want to store!'
問題待處理，但非必要
"""
"""
#創檔並儲存，已存在直接覆蓋
file = open("test_file.txt",'wb') #
file.write(contents)
file.close()
結果: data I want to store!
NO PROBLEM
"""


"""
待處理
#from flask import current_app as app from flask import send_file from myproject import Obj 
@app.route('/logo.png')
def logo():
     #Serves the logo image.
     obj = Obj.objects.get(title='Logo') 
     return send_file(io.BytesIO(obj.logo.read()), attachment_filename='logo.png', mimetype='image/png')



app.run("172.25.3.99",80)
"""
