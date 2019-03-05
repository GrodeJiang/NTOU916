# -*- coding: utf-8 -*-

from pymongo import MongoClient
from bson import ObjectId

class Database():
    
    def __init__(self, username):
            self.uri = "mongodb://localhost:27017/"
            self.client = MongoClient(self.uri)
            self.db = self.client[username]
    '''
    目前格式
    example = {'name':  'kinds_itemname_filename',
               'image': 'imageid',
               'list': {'data1': 'id1',
                        'data2': 'id2',
                        'data3': 'id3'}
               }
    '''
    #上傳 (database，名稱，圖片id，表格資料{dict})
    def Upload(self, name, imageid, listdata = None, price = None):
        doc = {'name': name,
               'image': imageid,
               'list': listdata}
        if price:
            doc['price'] = price
        result = self.db.doc.insert_one(doc)
        print ('upload done')
        return result.inserted_id
    
    #data = {data1, data2, ...}
    #id = {id1, id2, ...}
    ##list = {data1: id1, data2: id2, ...}
    def Makelist(*data_id):
        data_id = data_id
        listdata = {}
        for i in range(0,len(data_id[1])):
            listdata[data_id[1][i]] = data_id[2][i]
        else:
            return listdata
        print('Makelist fail')
        return None
    
    def Getdoc(self, key, value):
        try:
            for doc in self.db.doc.find({key: value}):
                return doc
        except:
            print('Getdoc fail')
            return None
    
    #拿資料 有target就回傳target的資料
    #否則回傳value資料
    #(database，尋找的關鍵字，尋找的值, 目標資料)
    def Getdata(self, key, value, key_to_get_data):    
        try:
            for doc in self.db.doc.find({key: value}):
                return doc[key_to_get_data]
        except:
            print('Getdata fail')
            return None
    
    def Getlistdata(self, key, value,list_target):    
        try:
            for doc in self.db.doc.find({key: value}):
                    if list_target is not None:            
                        return (doc['list'])[list_target]
        except:
            print('Getlistdata fail')
            return None
    #找到指定欄位，並修改
    #(database，尋找的關鍵字，尋找的值，修改後dist)
    def Modify(self, key, value, doc):
        try:
            self.db.doc.replace_one({key: value}, doc)
            return True
        except:
            print('Modify fail')
            return False
        
'''
testuser = Database('test')
info = ['Triangle','Rectangular','Circle']
data = [ObjectId("5af9bf0ba129741ec424679c"),
        ObjectId("5af9be7aa129741ec4243487"),
        ObjectId("5af86010a129741ec4240739")]
testlist = testuser.Makelist(info, data)



testdb = Database('test')
testdb.Upload('test', ObjectId("5ad778ada129740c4c85f7d8"), testlist)
'''