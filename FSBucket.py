# -*- coding: utf-8 -*-
from pymongo import MongoClient
from gridfs import GridFSBucket
from bson import ObjectId

class Filedata():
    def __init__(self, nums, filename, fileid, fileuploadtime):
        if nums is not None:
            self.nums = str(nums)
        self.filename = str(filename)
        self.fileid = str(fileid)
        self.fileuploadtime = str(fileuploadtime)

class FSBucket(Filedata):
    def __init__(self, username):
        self.username = username
        self.uri = "mongodb://localhost:27017/"
        self.client = MongoClient(self.uri)
        self.db = self.client[username]
        self.fs = GridFSBucket(self.db,'image')
        
    def Upload(self, fname):        
        with open(fname,'rb') as file:
            file_data = file.read()
            try:
                fileid = self.fs.upload_from_stream(self.username+'_'+fname,
                                                    file_data,
                                                    chunk_size_bytes=4,
                                                    metadata = {"contentType": "image"})
                print('upload done')
                return fileid
            except:
                print('err')
        return None
        
        
    def Findbyname(self, fname):
        data =[]
        i = 1 #計數器
        for grid_data in self.fs.find({"filename": fname}, 
                                      no_cursor_timeout = True):
            file = super(FSBucket, self).__init__(i, grid_data.filename, grid_data._id,
                                                grid_data.upload_date)
            data.append(file)
            i+=1
        else:
            return data;
    
        print("err")
        return None
    
    def Findbyid(self, fileid):
        grid_data = self.fs.find({"_id": fileid},
                                 no_cursor_timeout = True)
        file = super(FSBucket, self).__init__(None, grid_data.filename, grid_data._id,
                                                grid_data.upload_date)
        return file
    
    def Downloadbyname(self, fname):
        i = 1
        for grid_out in self.fs.find({"filename": fname}, 
                      no_cursor_timeout = True):
            contents_binary = grid_out.read()
            gname = grid_out.filename
            try:
                #開啟檔案，確認存在
                file = open(gname, 'r')
            except:
                #直接創新檔
                file = open(gname, 'wb')
            else:
                #已存在，另創新檔
                file.close()
                print("file already exist, so creat new file name:" + str(i) + "_" + gname)
                file = open(str(i) + "_" + gname, 'wb')
            file.write(contents_binary)
            file.close()
            i+=1
    
    def Delete(self, fname):
        for grid_data in self.fs.find({"filename": fname}, 
                             no_cursor_timeout = True):
            self.fs.delete(grid_data._id)
            print(str(grid_data.filename)+" has deleted")

#usertest = FSBucket('test')