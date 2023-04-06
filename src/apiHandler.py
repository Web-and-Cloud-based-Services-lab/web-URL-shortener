# Handler of API
# Defines the logics of CRUD

import pymongo
import json
import re
from tqdm import tqdm
from dbClient import mongo_client
from idController import idController
from base62Converter import base62Converter

class ApiHandler(object):
    def __init__(self):
        self.client = mongo_client
        self.db = self.client.url_shortener
        self.collection_urls = self.db.Urls

    # retrieve all keys (id in use) stored in database in the ascending order
    def get_keys(self):
        documents = self.collection_urls.find({}).sort("original_id",pymongo.ASCENDING)
        keys = []
        for document in documents:
          keys.append(document['short_id'])
        
        return json.dumps(keys, indent=2, ensure_ascii=False)

    # return the value of url based on the id value
    def get_url(self, short_id):
        query = { "short_id": short_id }
        document = self.collection_urls.find_one(query)
        if document == None:
            return None
        
        url = document['url']
        return url
    
    # get the id from id generator and encoded by base62 converter
    # insert the record into database 
    def create_url(self, url):
        id_origin = idController.generate_id()
        id_encoded = base62Converter.encode(id_origin)
        print("id: ", id_origin)
        print("encoded id: ", id_encoded)

        data = {'original_id': id_origin, 'short_id': id_encoded, 'url': url}
        self.collection_urls.insert_one(data)

        return id_encoded
    
    # only used at initiation for multiple data insertion
    def create_many_urls(self, urls):
        data = []
        # tqdm is a library to show progress bar
        # reference: https://stackoverflow.com/questions/43259717/progress-bar-for-a-for-loop-in-python-script
        for url in tqdm(urls):
            if self.verify_url(url):
                if not self.detect_duplicates(url):
                    id_origin = idController.generate_id()
                    id_encoded = base62Converter.encode(id_origin)
                    data.append({'original_id': id_origin, 'short_id': id_encoded, 'url': url})
        if len(data) != 0:
            self.collection_urls.insert_many(data)        

    # delete a record of url based on id
    # the released id is added to freelist
    def delete_url(self, short_id):
        query = { "short_id": short_id }
        self.collection_urls.delete_one(query)
        id_origin = base62Converter.decode(short_id)
        idController.add_to_freelist(id_origin)

    # update url based on id
    def edit_url(self, short_id, url):
        query = { "short_id": short_id }
        new_value = { "$set": { "url": url } }

        self.collection_urls.update_one(query, new_value)

    # verify if URL follows the regex pattern
    def verify_url(self, url):
        # set the regex pattern to validate url
        url_pattern = "^(?:(http|https)://)?(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
        # compile the regex pattern and returns a regex pattern object
        url_object = re.compile(url_pattern)
        # check the validation of the url    
        return re.search(url_object, url)            

    # check if url is already exist in database
    def detect_duplicates(self, url):
        documents = self.collection_urls.find({})
        for document in documents:
          if document['url'] == url:
              return True
        return False

apiHandler = ApiHandler()

