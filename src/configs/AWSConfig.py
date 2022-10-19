import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID_CONFIG")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY_CONFIG")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME_CONFIG")
