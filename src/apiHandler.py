import pymongo
import re
from idController import idController
from base62Converter import base62Converter

class ApiHandler(object):
    def __init__(self):
        self.client = pymongo.MongoClient('127.0.0.1',27017)

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
        id_encoded = self.get_id()
        url_formated = self.format_short_url(id_encoded, url)

        data = {'short_id': id_encoded, 'url': url}
        self.collection_urls.insert_one(data)

        return id_encoded

    def format_short_url(self, id, url):
        http_format = url.split('://', 1)[0]
        return http_format + "://" + id + ".com" 

    def get_id(self):
        id_origin = idController.get_id()
        id_encoded = base62Converter.encode(id_origin)
        print("id: ", id_origin)
        print("encoded id: ", id_encoded)
        return id_encoded

    # TODO: Implement this function!!
    def verify_url(self, url):
        # set the regex pattern to validate url
        url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
        # compile the regex pattern and returns a regex pattern object
        url_object = re.compile(url_pattern)
        # check the validation of the url
        if(re.search(url_object, url)):
            print(url, "is valid")
            return True
        else:
            print(url, "is not valid")
            return False
            

apiHandler = ApiHandler()