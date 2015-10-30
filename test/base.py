from ctx import database, view


class NeedsDatabase(object):
    @classmethod
    def setup_class(cls):
        database.init()

    def setup_method(self, method):
        database.server.delete(database.db.name)
        database.init()
        view.sync_views(database.db)
