# -*- coding: utf-8 -*-

from pymongo import MongoClient

class Database():
    
    def __init__(self, username):
            self.uri = "mongodb://localhost:27017/"
            self.client = MongoClient(self.uri)
            self.db = self.client[username]
    '''
    目前格式
    example = {'name':  'example',
               'image': 'imageid',
               'list': {'data1': 'id1',
                        'data2': 'id2',
                        'data3': 'id3'}
               }
    '''
    #上傳 (database，名稱，圖片id，表格資料{dict})
    def Upload(self, name, imageid, listdata):
        doc = {'name': name,
               'image': imageid,
               'list': listdata}
        result = self.db.doc.insert_one(doc)
        print ('upload done')
        return result.inserted_id
    
    #info = {info1, info2, ...}
    #data = {data1, data2, ...}
    ##list = {info1: data1, info2: data2, ...}
    def Makelist(*infodata):
        infodata = infodata
        datalist = {}
        for i in range(0,len(infodata[1])):
            datalist[infodata[1][i]] = infodata[2][i]
        else:
            return datalist
        print('err')
        return None    
    
    #拿資料 有target就回傳target的資料
    #否則回傳value資料
    #(database，尋找的關鍵字，尋找的值，表單目標[可略過])
    def Getdata(self, key, value, list_target=None):
        for doc in self.db.dbtest.find({key: value}):
            try:
                if list_target is not None:            
                    return (doc['list'])[list_target]
                else:
                    return doc[key]
            except:
                    print('err')
                    return None
    #找到指定欄位，並修改
    #(database，尋找的關鍵字，尋找的值，修改關鍵字，修改後的值)
    def Modify(self, key, value, modify_key, modify_value):
        for doc in self.db.dbtest.find({key: value}):
            doc_id = doc['_id']
            doc[modify_key] = modify_value
            self.db.dbtest.replace_one({'_id': doc_id}, doc)
        
'''
testuser = Database('test')
info = ['test1','test2','test3']
data = ['data1','data2','data3']
testlist = testuser.Makelist(info, data)



testdoc = {'test': '10', 'test2': '20'}
upload_doc('uptest', '', testdoc)
modify_doc("name", "uptest", "list", testdoc)
data = get_data("name", "uptest", "test")
'''