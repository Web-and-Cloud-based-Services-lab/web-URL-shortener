import pymongo

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
        print("verify called: ", url)
        if url == "a":
            return True
        return False

apiHandler = ApiHandler()