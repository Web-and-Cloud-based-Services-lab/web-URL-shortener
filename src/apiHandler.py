import pymongo
import re

class ApiHandler(object):
    def __init__(self):
        self.client = pymongo.MongoClient('127.0.0.1',8888)

        self.db = self.client.url_shortener
        self.collection_urls = self.db.Urls

    def test_db_connection(self):
        collections = self.db.collection_names(include_system_collections=False)
        for collect in collections:
            print(collect)


    
    def create_url(self, data):
        url = data['url']
        if self.verify_url(url):
            print("url is valid")
        else:
            print("url is not valid")
        self.get_id(url)



    def get_id(self, url):
        return url

    # TODO: Implement this function!!
    def verify_url(self, url):
        # set the regex pattern to validate url
        url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
        # compile the regex pattern and returns a regex pattern object
        url_object = re.compile(url_pattern)
        # check the validation of the url
        if(re.search(url_object, url)):
            return True
        else:
            return False

apiHandler = ApiHandler()