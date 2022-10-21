from datetime import datetime
from boto3.dynamodb.conditions import Attr
from ..controllers import AWSController


def getMessages(roomname):
    status = 'error'
    message = f'Failed to get messages for room {roomname}'
    data = []
    size = 0
    try:
        response = AWSController.MessagesController.scan(
            FilterExpression=Attr('room_name').eq(roomname)
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                data = response['Items']
                size = response['Count']
                status = 'success'
                message = ''
    except Exception as e:
        status = 'error'
        message = str(e)
    return sorted(data, key=lambda x: x['create_date'], reverse=False), size, status, message


def addMessage(username, roomname, text):
    status = 'error'
    message = f'Failed to add message to room {roomname}'
    try:
        response = AWSController.MessagesController.put_item(
            Item={
                'create_date': str(datetime.now()),
                'user_name': username,
                'room_name': roomname,
                'message': text
            }
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            status = 'success'
            message = ''
    except Exception as e:
        status = 'error'
        message = str(e)
    return status, message
