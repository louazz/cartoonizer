from flask_bcrypt import Bcrypt
from tinydb import TinyDB, Query
import uuid
from datetime import datetime
import json 

db_2 = TinyDB('users.json')

def addUser( email, username, password):
    db_2.insert({"id": uuid.uuid4().hex, 'email': email, 
                 "username": username, "password": password})

def findUser(username, password, bcrypt):
    User = Query()
    user = db_2.search((User.username == username))
    if bcrypt.check_password_hash(user[0]["password"], password):
        print(user)
        return user
    else: 
        return None
    
db = TinyDB("photo.json")

def addPhoto(name, user):
    id = uuid.uuid4()
    db.insert({"id": id.hex, "name": name, "date":json.dumps(datetime.now(), indent=4, sort_keys=True, default=str), "user": user})
    return id.hex


def findById(user):
    Photo = Query()
    photo = db.search(Photo.user==user)
    return photo

def findByPhoto(id):
    Photo = Query()
    photo = db.search(Photo.id==id)[0]
    return photo

def removePhoto(id):
    Photo = Query()
    db.remove(Photo.id == id)