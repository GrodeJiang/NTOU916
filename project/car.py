# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 20:33:25 2018

@author: user
"""

from Users import Users
from pymongo import MongoClient

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client['Users']

def addcar(username, itemid):
    if username is None:
        print("username is None")
        return False
    doc = db.doc.find_one({'username': username})
    if doc is not None:
        try:
            carlist =  doc['car']
        except KeyError:
            carlist = []
        carlist.append(itemid)
        doc['car'] = carlist
        db.doc.find_one_and_replace({'username': username}, doc)
        return True
    print("username not found")
    return False
    
def delcar(username, itemid):
    if username is None:
        print("username is None")
        return False
    doc = db.doc.find_one({'username': username})
    if doc is not None:
        try:
            carlist =  doc['car']
        except KeyError:
            return False
        try:
            i = carlist.index(itemid)
        except ValueError:
            print('not found')
            return False
        carlist.pop(i)
        doc['car'] = carlist
        db.doc.find_one_and_replace({'username': username}, doc)
        return True
    print("username not found")
    return False
    