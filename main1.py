# coding=utf-8
from flask import Flask
from pymongo import MongoClient
from gridfs import GridFSBucket

app = Flask(__name__)

@app.route('/')

def root():
    
	return "Hello World!!"

uri = "mongodb://BB1:a12151456@172.25.3.41/?authSource=test"

client = MongoClient(uri)



db = client['test']



#存進id作分類

fs.exists({"_id": "lisa.txt"}
#讀取lisa.txt
for grid_out in fs.find({"filename": "lisa.txt"},
                        no_cursor_timeout=True):
    data = grid_out.read()
#將檔案上傳



my_db = MongoClient().test fs = GridFSBucket(my_db)
grid_in, file_id = fs.open_upload_stream( "test_file", 

chunk_size_bytes=4, metadata={"contentType": "text/plain"}) 

grid_in.write("data I want to store!") 

grid_in.close() # uploaded on close






#將檔案上傳至stream?

my_db = MongoClient().test 
fs = GridFSBucket(my_db) # get _id of file to read. file_id = fs.upload_from_stream("test_file", "data I want to store!") 
grid_out = fs.open_download_stream(file_id) contents = grid_out.read()





#將檔案從db下載

#from flask import current_app as app from flask import send_file from myproject import Obj 
@app.route('/logo.png')
 def logo(): """Serves the logo image.""" obj = Obj.objects.get(title='Logo') return send_file(io.BytesIO(obj.logo.read()), attachment_filename='logo.png', mimetype='image/png')








app.run("172.25.3.99",80)

