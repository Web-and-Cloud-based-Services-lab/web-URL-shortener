import pymongo

class Logic(object):
    def __init__(self):
        self.client = pymongo.MongoClient('127.0.0.1',8888)

        self.db = self.url_shortener
        self.collection_urls = self.db.Urls

    def test_db_connection(self):
        collections = self.db.collection_names(include_system_collections=False)
        for collect in collections:
            print(collect)