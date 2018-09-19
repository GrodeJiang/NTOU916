# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
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
    __tablename__ = 'users'
    id = None
    email = None
    username = None
    password_hash = None
    role_id = None
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def virify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def login(self, username, password):
        print(username + "\n" + password)
        doc = db.doc.find_one({'username': username})
        print(doc)
        if doc is not None:
            self.password(doc['password'])
            if self.virify_password(password):
                print('Login success')
                self.id = username
                self.username = username
                return True
            print('Login fail')
            return False
        print('User not found')
        return False
    
    def register(self, username, password):
        flag = db.doc.find_one({'username': username})
        if flag is None:
            doc = { 'username': username,
                    'password': password}
            db.doc.insert_one(doc)
            return True
        else:
            print(flag)
            print('User aleady exists')
            return False
        '''
        try:
            doc = db.doc.find_one({'username': username})
        except TypeError:
            doc = { 'username': username,
                    'password': generate_password_hash(password) }
            db.doc.insert_one(doc)
            return True
        else:
            print(doc)
            print('User aleady exists')
            return False
        '''
    def check(self, username):
         doc = db.doc.find_one({'username': username})
         if doc is not None:
             return True
         return False

