from dbClient import mongo_client

class IdController(object):
    def __init__(self):
        self.client = mongo_client
        self.db = self.client.url_shortener
        self.collection_urls = self.db.Urls   

        self.next = 0
        self.freelist = []

        documents = self.collection_urls.find({})
        ids = []
        for document in documents:
            ids.append(document['original_id'])
        if len(ids) != 0:
            print("ids in db: ", ids)
            self.next = max(ids) + 1
            print("init next: ", self.next)
            self.freelist = self.generate_freelist(ids)
            print("init freelist: ", self.freelist)
            
    def generate_freelist(self, ids):
        ids_set = set(ids)
        full_set = set(list(range(self.next)))

        return list(full_set - ids_set)

    def has_vacancy(self):
        return len(self.freelist) != 0
    
    def generate_id(self):
        res = 0
        if self.has_vacancy():
            res = min(self.freelist)
            index = self.freelist.index(res)
            self.freelist.pop(index)
        else:
            res = self.next
            self.next += 1
        return res
    
    def add_to_freelist(self, id_origin):
        self.freelist.append(id_origin)

idController = IdController()