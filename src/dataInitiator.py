from apiHandler import apiHandler

class DataInitiator:
    def __init__(self):   
        self.urls = ['http://www.hilihili.com', 'http://www.vu.co.jp', 'http://www.helloworld.net'] 

    def sample_urls_to_database(self):
        apiHandler.create_many_urls(self.urls)

dataInitiator = DataInitiator()