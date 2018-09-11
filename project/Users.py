# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from pymongo import MongoClient

'''
    example = {'username': 'username',
               'Password': 'password_hash' }
'''

#uri = "mongodb://BB1:a4502143@172.25.3.206/?authSource=test"
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client['Users']

class Users(UserMixin):
    #username = None
    password_hash = None
    def login(self, username, password):
        doc = db.doc.find_one("Username", username)
        if doc is not None:
            if check_password_hash(doc[password], password):
                print('Login success')
                return True
            print('Login fail')
            return False
        print('User not found')
        return False
    
    def register(self, username, password):
        try:
            db.doc.find({'username': username})
        except TypeError:
            doc = { 'username': username,
                    'password': generate_password_hash(password) }
            db.doc.insert_one(doc)
            return True
        else: 
            print('User aleady exists')
            return False
    def password(self, password):
        self.password_hash = generate_password_hash(password)
