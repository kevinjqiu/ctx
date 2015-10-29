from ctx import database


class NeedsDatabase(object):
    @classmethod
    def setup_class(cls):
        database.init()

    def setup_method(self, method):
        for id in database.db:
            del database.db[id]
