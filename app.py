from flask import Flask, send_file, Response
from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager
from db import addUser, findUser, addPhoto, findByPhoto, removePhoto, findById
from flask_jwt_extended import jwt_required
import subprocess
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os 
from cartoonize import cartoonize

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY']= "louai"
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1000)
jwt = JWTManager(app)
@app.route("/api/login", methods = ["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    user = findUser(username=username, password=password,bcrypt=bcrypt)
    if not user:
        return jsonify({"msg": "User does not exist"}), 401
    
    access_token = create_access_token(identity=user[0]['id'])
    return jsonify({"token": access_token}), 200

@app.route("/api/signup", methods= ["POST"])
def singup():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    pw_hash = bcrypt.generate_password_hash(password)


    addUser(email=email, password=pw_hash.decode("utf-8"), username=username)
    return jsonify({"msg": "User created"}), 200

@app.route("/api/photo/find", methods = ["GET"])
@jwt_required()
def search():
    user = get_jwt_identity()
    photos = findById(user)
    return jsonify({"photos": photos}), 200

@app.route("/api/photo/id", methods = ["GET"])
@jwt_required()
def findDoc():
    request.args.get('id')
    photo = findByPhoto(request.para)
    return jsonify({"photo": photo}), 200

@app.route("/api/photo", methods = ["POST"])
@jwt_required()
def CreatePhoto():
    user = get_jwt_identity()
    file = request.files['file']
    print(file.filename)
    type = file.filename.split(".")[-1] 
    print(type)
    id = addPhoto(name= str(file.filename), user= user)
    print(id)
    subprocess.run(["mkdir", "./uploads/"+ str(id)]) 
    file.save("./uploads/"+ str(id)+"/"+file.filename)
    cartoonize("./uploads/"+ str(id)+"/cartoonized."+type, "./uploads/"+ str(id)+"/"+file.filename)
    return send_file("./uploads/"+ str(id)+"/cartoonized."+type, as_attachment=True, download_name="cartoonized."+type)

@app.route("/api/photo/download", methods=["POST"])
def download():
    id = request.json.get("id", None)
    name = request.json.get("name", None)
    print(id)
    print(name)

    type = name.split(".")[-1]
    file_path ="./uploads/"+ str(id)+"/cartoonized."+type
    print(os.path.isfile(file_path))
    if os.path.isfile(file_path):
        print("valid path")
        return send_file(file_path, download_name=name, as_attachment=True)

@app.route("/api/photo/delete", methods= ["POST"])
@jwt_required()
def delete():
    id = request.json.get("id", None)
    path = "./uploads/"+ str(id)
    subprocess.run(["rm","-r", path]) 
    removePhoto(id)
    return jsonify({"msg": "file deleted!"}), 200


app.run(debug=True, port=5000, host="0.0.0.0")