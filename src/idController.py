class IdController(object):
    def __init__(self):
        self.next = 0
        self.freelist = []

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