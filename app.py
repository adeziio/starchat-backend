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

from src.servers import UserServer
from src.servers import MessageServer
from src.utils import GithubService


app = Flask(__name__)
load_dotenv(find_dotenv())
CORS(app, origins=[os.getenv("UI_HOST_URL")], methods=['GET', 'POST'], allow_headers=[
     'Content-Type', 'Authorization', 'x-csrf-token'], supports_credentials=True)

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = "None"
app.config['JWT_ACCESS_COOKIE_PATH'] = "/api/"
app.config['JWT_REFRESH_COOKIE_PATH'] = "/token/refresh"
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_COOKIE_CSRF_PROJECT'] = True if os.getenv(
    "ENV") == "prod" else False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)


@app.route('/registerUser', methods=['POST'])
def registerUser():
    body = request.json
    username = body['username']
    password = body['password']
    if (username and password):
        status, message = "", ""
        return jsonify(status=status, message=message)
    return jsonify(status="error", message="Missing Fields")


@app.route('/login', methods=['POST'])
def login():
    body = request.json
    username = body['username']
    password = body['password']
    if (username and password):
        ls, lenLs, status, message = UserServer.get(username)
        if (status == "success" and lenLs > 0):
            if (ls[0]['pass_word'] == password):

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
@jwt_required
def user():
    return jsonify(username=get_jwt_identity())


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
    UserServer.init()
    MessageServer.init()
    GithubService.pushToGithub()
    app.run()
