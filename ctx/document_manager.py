from ctx import document


class DocumentManager(object):
    def __init__(self, db):
        self.db = db

    def get_tasks(self):
        return self.db.view('_all_docs', include_docs=True,
                            wrapper=document.Task)
