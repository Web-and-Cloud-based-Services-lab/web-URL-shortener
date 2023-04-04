class IdController(object):
    def __init__(self):
        self.next = 0
        self.vacancies = [8888,9999,2222,33333333]

    def has_vacancy(self):
        return len(self.vacancies) != 0
    
    def get_id(self):
        res = 0
        if self.has_vacancy():
            res = min(self.vacancies)
            index = self.vacancies.index(res)
            self.vacancies.pop(index)
        else:
            res = self.next
            self.next += 1
        return res
idController = IdController()