from ctx import database


class NeedsDatabase(object):
    @classmethod
    def setup_class(cls):
        database.init()

    def setup_method(self, method):
        database.server.delete(database.db.name)
        database.init()
