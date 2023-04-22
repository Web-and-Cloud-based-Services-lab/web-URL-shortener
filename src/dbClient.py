# settings of mongoDB client

import pymongo 

username = 'url_shortener'
password = 'url_shortener_passwor'

mongo_client = pymongo.MongoClient('mongodb://{user}:{pwd}@localhost:27017/admin'.format(user = username, pwd = password))