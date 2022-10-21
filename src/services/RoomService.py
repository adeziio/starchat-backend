from datetime import datetime
from ..controllers import AWSController


def hasRoom(roomname):
    ret = False
    try:
        response = AWSController.RoomsController.get_item(
            Key={
                'room_name': roomname
            },
            AttributesToGet=[
                'room_name'
            ]
        )
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Item' in response):
                if (response['Item']['room_name'] == roomname):
                    ret = True
    except Exception:
        ret = False
    return ret


def getAllRoom():
    status = 'error'
    message = 'Failed to get all rooms'
    data = []
    size = 0
    try:
        response = AWSController.RoomsController.scan()
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                data = response['Items']
                size = response['Count']
                status = 'success'
                message = ''
    except Exception as e:
        status = 'error'
        message = str(e)
    return sorted(data, key=lambda x: x['create_date'], reverse=True), size, status, message


def addRoom(username, roomname):
    status = 'error'
    message = 'Failed to add room'
    if (not hasRoom(roomname)):
        try:
            response = AWSController.RoomsController.put_item(
                Item={
                    'room_name': roomname,
                    'create_date': str(datetime.now()),
                    'created_by': username
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
        message = 'Room Name Already Exists'
    return status, message
