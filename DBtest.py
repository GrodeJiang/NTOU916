# -*- coding: utf-8 -*-

from pymongo import MongoClient

uri = "mongodb://localhost:27017/" #個人測試用
username = 'test'
client = MongoClient(uri)
db = client[username]

'''
目前格式
example = {'name':  'example',
           'image': 'imageid',
           'list': {'data1': 'id1',
                    'data2': 'id2',
                    'data3': 'id3'}
           }
'''

#上傳 (名稱，圖片id，表格資料{dict})
def upload_doc(name, imageid, listdata):
    doc = {'name': name,
           'image': imageid,
           'list': listdata}
    result = db.dbtest.insert_one(doc)
    print ('upload done')
    return result.inserted_id


#拿資料 有target就回傳target的資料
#否則回傳value資料
#(尋找的關鍵字，尋找的值，表單目標[可略過])
def get_data(key, value, list_target=None):
    for doc in db.dbtest.find({key: value}):
        try:
            if list_target is not None:            
                return (doc['list'])[list_target]
            else:
                return doc[key]
        except:
                print('err')
                return None
#找到指定欄位，並修改
#(尋找的關鍵字，尋找的值，修改關鍵字，修改後的值)
def modify_doc(key, value, modify_key, modify_value):
    for doc in db.dbtest.find({key: value}):
        doc_id = doc['_id']
        doc[modify_key] = modify_value
        db.dbtest.replace_one({'_id': doc_id},doc)

'''
testdoc = {'test': '10', 'test2': '20'}
upload_doc('uptest', '', testdoc)
modify_doc("name", "uptest", "list", testdoc)
data = get_data("name", "uptest", "test")
'''