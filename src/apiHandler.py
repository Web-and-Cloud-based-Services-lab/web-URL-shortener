import pymongo
import json
import re
from dbClient import mongo_client
from idController import idController
from base62Converter import base62Converter

class ApiHandler(object):
    def __init__(self):
        self.client = mongo_client
        self.db = self.client.url_shortener
        self.collection_urls = self.db.Urls

    def get_keys(self):
        documents = self.collection_urls.find({})
        keys = []
        for document in documents:
          keys.append(document['short_id'])
        print(keys)
        
        return json.dumps(keys, indent=2, ensure_ascii=False)

    def get_url(self, short_id):
        query = { "short_id": short_id }
        document = self.collection_urls.find_one(query)
        if document == None:
            return None
        
        url = document['url']
        return url
    
    def create_url(self, url):
        id_origin = idController.generate_id()
        id_encoded = base62Converter.encode(id_origin)
        print("id: ", id_origin)
        print("encoded id: ", id_encoded)
        
        # url_formated = self.format_short_url(id_encoded, url)
        data = {'original_id': id_origin, 'short_id': id_encoded, 'url': url}
        self.collection_urls.insert_one(data)

        return id_encoded

    def delete_url(self, short_id):
        query = { "short_id": short_id }
        self.collection_urls.delete_one(query)
        id_origin = base62Converter.decode(short_id)
        idController.add_to_freelist(id_origin)

    def edit_url(self, short_id, url):
        query = { "short_id": short_id }
        new_value = { "$set": { "url": url } }

        self.collection_urls.update_one(query, new_value)

    def format_short_url(self, id, url):
        http_format = url.split('://', 1)[0]
        return http_format + "://" + id + ".com" 

    def verify_url(self, url):
        # set the regex pattern to validate url
        url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
        # compile the regex pattern and returns a regex pattern object
        url_object = re.compile(url_pattern)
        # check the validation of the url    
        return re.search(url_object, url)            

    def detect_duplicates(self, url):
        documents = self.collection_urls.find({})
        for document in documents:
          if document['url'] == url:
              return True
        return False

apiHandler = ApiHandler()

