import os
from flask import Flask, jsonify, make_response, request
from dotenv import load_dotenv, find_dotenv
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from datetime import timedelta
from flask_mail import Mail, Message

from src.services import UserService
from src.services import MessageService
from src.services import RoomService


app = Flask(__name__)
load_dotenv(find_dotenv())

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = "None"
app.config['JWT_ACCESS_COOKIE_PATH'] = "/api/"
app.config['JWT_REFRESH_COOKIE_PATH'] = "/token/refresh"
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)


app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('FREEFLASH_MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('FREEFLASH_MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/")
def default():
    return "Server is online..."


@app.route('/forgotUsernameAndPassword', methods=['POST'])
def forgotUsernameAndPassword():
    body = request.json
    email = body['email']
    if (email):
        user_name, pass_word, status, message = UserService.getEmail(email)
        msg = Message(
            f'Starchat',
            sender=os.getenv('FREEFLASH_MAIL_USERNAME'),
            recipients=[email]
        )
        html = '<html>'
        html += '<head>'
        html += '<title>Star Chat</title>'
        html += '</head>'
        html += '<body>'
        html += '<a href="https://starchat.vercel.app/" style="text-decoration:none; font-size: 7rem; color: #1976d2; font-family: cursive;">Star Chat</a>'
        html += f'<p style="font-size: 3rem; margin: 0rem;"><span style="font-weight: bold;">Username:</span> {user_name}</p>'
        html += f'<p style="font-size: 3rem; margin: 0rem;"><span style="font-weight: bold;">Password:</span> {pass_word}</p>'
        html += '</body>'
        html += '</html>'
        msg.html = html

        try:
            mail.send(msg)
        except:
            jsonify(status="error", message="Failed to send email")

        return jsonify(status=status, message=message)
    return jsonify(status="error", message="Missing Fields")


@app.route('/registerUser', methods=['POST'])
def registerUser():
    body = request.json
    username = body['username']
    password = body['password']
    email = body['email']
    if (username and password and email):
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


@app.route('/api/addMessage', methods=['POST'])
@jwt_required()
def addMessage():
    username = get_jwt_identity()
    body = request.json
    roomname = body['roomname']
    text = body['message']
    status, message = MessageService.addMessage(username, roomname, text)
    return jsonify(status=status, message=message)


@app.route('/api/viewRooms', methods=['GET'])
@jwt_required()
def viewRooms():
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
