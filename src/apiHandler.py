# Handler of API
# Defines the logics of CRUD

import pymongo
import json
import re
from tqdm import tqdm
from dbClient import mongo_client
from idGenerator import idGenerator
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
        id_origin = idGenerator.generate_id()
        id_encoded = base62Converter.encode(id_origin)
        print("id: ", id_origin, " encoded id: ", id_encoded)
        print("url: ", url)

        data = {'original_id': id_origin, 'short_id': id_encoded, 'url': url}
        self.collection_urls.insert_one(data)

        return id_encoded
    
    # only used at initiation for multiple data insertion
    def create_many_urls(self, urls):
        # tqdm is a library to show progress bar
        # reference: https://stackoverflow.com/questions/43259717/progress-bar-for-a-for-loop-in-python-script
        for url in tqdm(urls):
            if self.verify_url(url):
                duplicate = self.detect_duplicates(url)
                if not duplicate['exists']:
                    id_origin = idGenerator.generate_id()
                    id_encoded = base62Converter.encode(id_origin)
                    data = {'original_id': id_origin, 'short_id': id_encoded, 'url': url}
                    self.collection_urls.insert_one(data)       

    # delete a record of url based on id
    def delete_url(self, short_id):
        query = { "short_id": short_id }
        self.collection_urls.delete_one(query)

    # update url based on id
    def edit_url(self, short_id, url):
        query = { "short_id": short_id }
        document = self.collection_urls.find_one(query)
        origin_url = document['url']
        new_value = { "$set": { "url": url } }

        self.collection_urls.update_one(query, new_value)
        return origin_url

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
              return {"exists": True, "short_id": document['short_id']}
        return {"exists": False}

apiHandler = ApiHandler()

