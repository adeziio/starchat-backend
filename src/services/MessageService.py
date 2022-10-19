from datetime import datetime
from ..controllers import AWSController


def getMessages(roomname):
    status = 'error'
    message = f'Failed to get messages for room {roomname}'
    try:
        response = AWSController.MessagesController.get_item(
            Key={
                'room_name': roomname
            },
            AttributesToGet=[
                'user_name', 'room_name', 'create_date', 'message'
            ]
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            data = response['Items']
            size = response['Count']
            status = 'success'
            message = ''
    except Exception as e:
        status = 'error'
        message = str(e)
    return data, size, status, message


def addMessage(username, roomname, message):
    status = 'error'
    message = f'Failed to add message to room {roomname}'
    try:
        createdate = str(datetime.now())
        response = AWSController.MessagesController.put_item(
            Item={
                'user_name': username,
                'room_name': roomname,
                'create_date': createdate,
                'message': message
            }
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            status = 'success'
            message = ''
    except Exception as e:
        status = 'error'
        message = str(e)
    return status, message
