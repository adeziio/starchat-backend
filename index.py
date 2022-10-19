import os
from time import time
from flask import Flask, jsonify, make_response, request
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from datetime import timedelta

from src.services import UserService
from src.services import MessageService
from src.services import RoomService


app = Flask(__name__)
load_dotenv(find_dotenv())
# CORS(app, origins=[os.getenv("UI_HOST_URL")], methods=['GET', 'POST'], allow_headers=[
#      'Content-Type', 'Authorization', 'x-csrf-token'], supports_credentials=True)

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = "None"
app.config['JWT_ACCESS_COOKIE_PATH'] = "/api/"
app.config['JWT_REFRESH_COOKIE_PATH'] = "/token/refresh"
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)


@app.route("/")
def default():
    return "Server is online..."


@app.route('/registerUser', methods=['POST'])
def registerUser():
    body = request.json
    username = body['username']
    password = body['password']
    email = body['email']
    if (username and password):
        status, message = UserService.addUser(username, password, email)
        return jsonify(status=status, message=message)
    return jsonify(status="error", message="Missing Fields")


@app.route('/login', methods=['POST'])
def login():
    body = request.json
    username = body['username']
    password = body['password']
    if (username != "" and password != ""):
        user_name, pass_word, status, message = UserService.getUser(username)
        if (status == "success"):
            if (username == user_name and pass_word == password):
                access_token = create_access_token(identity=username)
                refresh_token = create_refresh_token(identity=username)
                response = jsonify(username=username,
                                   status=status, message=message)
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                return response
        return jsonify(status="error", message="Invalid Username or Password")
    return jsonify(status="error", message="Missing Fields")


@app.route('/logout', methods=['GET'])
def logout():
    response = jsonify(logout=True)
    unset_jwt_cookies(response)
    return response


@app.route('/api/user', methods=['GET'])
@jwt_required()
def user():
    return jsonify(username=get_jwt_identity())


@app.route('/api/viewMessages', methods=['POST'])
@jwt_required()
def viewMessages():
    body = request.json
    roomname = body['roomname']
    data, size, status, message = MessageService.getMessages(roomname)
    return jsonify(data=data, size=size, status=status, message=message)


@app.route('/api/viewAllRoom', methods=['GET'])
@jwt_required()
def viewAllRoom():
    data, size, status, message = RoomService.getAllRoom()
    return jsonify(data=data, size=size, status=status, message=message)


@app.route('/api/addRoom', methods=['POST'])
@jwt_required()
def addRoom():
    username = get_jwt_identity()
    body = request.json
    roomname = body['roomname']
    status, message = RoomService.addRoom(username, roomname)
    return jsonify(status=status, message=message)


@app.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    username = get_jwt_identity()
    access_token = create_access_token(identity=username)
    response = jsonify(refresh=True)
    set_access_cookies(response, access_token)
    return response


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


if __name__ == '__main__':
    app.run()
