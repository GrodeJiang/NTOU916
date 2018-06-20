# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from pymongo import MongoClient

'''
    example = {'username': 'username',
               'Password': 'password_hash' }
'''

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client['Users']

class User(UserMixin): 
    username = None
    password_hash = None
    def Login(self, username, password):
        doc = db.doc.find_one("Username", username)
        if doc is not None:
            if check_password_hash(doc[password], password):
                print('Login success')
                return True
            print('Login fail')
            return False
        print('User not found')
        return False
    
    def Register(self, username, password):
        flag = db.doc.find_one("Username", username)
        if flag is not None:
            print('User aleady exists')
            return False
        doc = { 'username': username,
                'password': generate_password_hash(password) }
        db.doc.insert_one(doc)
        return True
        
    def password(self, password):
        self.password_hash = generate_password_hash(password)
