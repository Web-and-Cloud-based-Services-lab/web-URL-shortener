# controls ID generation
# id is allocated in an ascending order
# deleted id is reused and smaller id has higher priority than bigger ones

from dbClient import mongo_client

class IdGenerator(object):
    def __init__(self):
        self.client = mongo_client
        self.db = self.client.url_shortener
        self.collection_urls = self.db.Urls   
    
    # find free ids by subtraction of sets
    def generate_freelist(self, ids, next_id):
        ids_set = set(ids)
        full_set = set(list(range(next_id)))

        return list(full_set - ids_set)
    
    # check the reusable id first and if none, allocate a id = current max + 1
    def generate_id(self):
        next_id = 0
        documents = self.collection_urls.find({})
        freelist = []
        ids = []

        for document in documents:
            ids.append(document['original_id'])
        if len(ids) != 0:
            next_id = max(ids) + 1
            freelist = self.generate_freelist(ids, next_id)
        if len(freelist) != 0:
            next_id = min(freelist)
        
        return next_id
    
idGenerator = IdGenerator()