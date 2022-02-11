from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json

app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb://db:27017")
db = client.ImageRecognition
users = db["Users"]


def check_valid_user(username):
    return users.find({"Username": username}).count() == 0


class Register(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]

        if check_valid_user(username) is False:
            return_json = {
                "status": 301,
                "message": "Error: Username already exists!"
            }
            return jsonify(return_json)

        hashed_password = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_password,
            "Tokens": 5
        })

        return_json = {
            "status": 200,
            "message": "Successfully signed up for the API!"
        }
        return jsonify(return_json)
