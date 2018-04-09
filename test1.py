# coding=utf-8
from flask import Flask
from pymongo import MongoClient
from gridfs import GridFSBucket
from gridfs import GridFS

app = Flask(__name__)

@app.route('/')

def root():
    
	return "Hello World!!"

uri = "mongodb://localhost:27017/"

client = MongoClient(uri)

db = client['test']

gfs = GridFS(db , collection='gfs')

#存進id作分類
if gfs.exists({"_id": "uptest.txt"}):
    #讀取lisa.txt
    print ('hello')
    for grid_out in gfs.find({"filename": "lisa.txt"},
                            no_cursor_timeout=True):
        data = grid_out.read()
        #將檔案上傳



#my_db = MongoClient().test
fs = GridFSBucket(db)
grid_in = fs.open_upload_stream( "uptest.txt",
                                chunk_size_bytes=4,
                                metadata={"contentType": "text/plain"}) 

grid_in.write('data I want to store!'.encode("UTF-8")) 

grid_in.close() # uploaded on close

for grid_data in fs.find({"filename": "uptest.txt"},
                         no_cursor_timeout=True):
    print('hello')





"""
#將檔案上傳至stream?

my_db = MongoClient().test 
fs = GridFSBucket(my_db) # get _id of file to read. file_id = fs.upload_from_stream("test_file", "data I want to store!") 
grid_out = fs.open_download_stream(file_id)
contents = grid_out.read()





#將檔案從db下載

#from flask import current_app as app from flask import send_file from myproject import Obj 
@app.route('/logo.png')
def logo():
     #Serves the logo image.
     obj = Obj.objects.get(title='Logo') 
     return send_file(io.BytesIO(obj.logo.read()), attachment_filename='logo.png', mimetype='image/png')








app.run("localhost:27017",80)
"""
