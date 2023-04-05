from apiHandler import apiHandler
import pandas as pd

urls = pd.read_csv("../data/URLs.csv", names = ['url', 'class'])

class DataInitiator:
    def __init__(self):   
        # self.urls = ['http://www.hilihili.com', 'http://www.vu.co.jp', 'http://www.helloworld.net'] 
        self.urls = urls['url'].tolist()[:10000]

    def sample_urls_to_database(self):
        apiHandler.create_many_urls(self.urls)

dataInitiator = DataInitiator()