# settings of mongoDB client

import pymongo 
import os

username = 'url_shortener'
password = 'url_shortener_password'

# mongo_client = pymongo.MongoClient('mongodb://{user}:{pwd}@mongo:27017/admin'.format(user = username, pwd = password))
mongo_client = pymongo.MongoClient('mongodb://{url}'.format(url=os.environ['DB_URL']))
# mongo_client = pymongo.MongoClient('mongodb://{user}:{pwd}@{url}'.format(user = os.environ['USER_NAME'], pwd = os.environ['USER_PWD'], url = os.environ['DB_URL']))