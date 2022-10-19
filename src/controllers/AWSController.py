from boto3 import resource
from ..configs import AWSConfig

AWS_ACCESS_KEY_ID = AWSConfig.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = AWSConfig.AWS_SECRET_ACCESS_KEY
AWS_REGION_NAME = AWSConfig.AWS_REGION_NAME

resource = resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

UsersController = resource.Table("starchat-users")
RoomsController = resource.Table("starchat-rooms")
MessagesController = resource.Table("starchat-messages")
