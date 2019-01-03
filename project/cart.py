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

def addcart(username, itemid):
    if username is None:
        print("username is None")
        return False
    doc = db.doc.find_one({'username': username})
    if doc is not None:
        try:
            cartlist =  doc['cart']
        except KeyError:
            cartlist = []
        cartlist.append(itemid)
        doc['cart'] = cartlist
        db.doc.find_one_and_replace({'username': username}, doc)
        return True
    print("username not found")
    return False
    
def delcart(username, itemid):
    if username is None:
        print("username is None")
        return False
    doc = db.doc.find_one({'username': username})
    if doc is not None:
        try:
            cartlist =  doc['cart']
        except KeyError:
            return False
        try:
            i = cartlist.index(itemid)
        except ValueError:
            print('not found')
            return False
        cartlist.pop(i)
        doc['cart'] = cartlist
        db.doc.find_one_and_replace({'username': username}, doc)
        return True
    print("username not found")
    return False
    