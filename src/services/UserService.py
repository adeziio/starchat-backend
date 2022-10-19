import os
from datetime import datetime
from cryptography.fernet import Fernet
from dotenv import load_dotenv, find_dotenv
from ..controllers import AWSController

load_dotenv(find_dotenv())

key = bytes(os.getenv("USER_CRYPTO_KEY"), encoding='utf-8')
fernet = Fernet(key)


def hasUser(username):
    ret = False
    try:
        response = AWSController.UsersController.get_item(
            Key={
                'user_name': username
            },
            AttributesToGet=[
                'user_name'
            ]
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Item' in response):
                if (response['Item']['user_name'] == username):
                    ret = True
    except Exception as e:
        ret = False
    return ret


def getUser(username):
    status = 'error'
    message = 'Failed to retrieve user'
    user_name = ''
    pass_word = ''
    try:
        response = AWSController.UsersController.get_item(
            Key={
                'user_name': username
            },
            AttributesToGet=[
                'user_name', 'create_date', 'last_updated_date', 'pass_word', 'email'
            ]
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Item' in response):
                user_name = response['Item']['user_name']
                pass_word = fernet.decrypt(
                    bytes(response['Item']['pass_word'], encoding='utf-8')).decode()
                status = 'success'
                message = ''
    except Exception as e:
        status = 'error'
        message = str(e)
    return user_name, pass_word, status, message


def addUser(username, password, email):
    status = 'error'
    message = 'Failed to add user'
    if (not hasUser(username)):
        try:
            createdate = str(datetime.now())
            response = AWSController.UsersController.put_item(
                Item={
                    'user_name': username,
                    'create_date': createdate,
                    'last_updated_date': createdate,
                    'pass_word': fernet.encrypt(password.encode()).decode("utf-8"),
                    'email': email
                }
            )
            if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
                status = 'success'
                message = ''
        except Exception as e:
            status = 'error'
            message = str(e)
    else:
        status = 'error'
        message = 'Username Already Exists'
    return status, message
