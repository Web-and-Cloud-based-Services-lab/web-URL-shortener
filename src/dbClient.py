# settings of mongoDB client

import pymongo 

username = 'url_shortener'
password = 'url_shortener_password'

mongo_client = pymongo.MongoClient('mongodb://{user}:{pwd}@mongo:27017/admin'.format(user = username, pwd = password))