from ctx import document


class DocumentManager(object):
    def __init__(self, db):
        self.db = db

    def get_tasks(self):
        return self.db.view('_all_docs', include_docs=True)

    def create_task(self, **kwargs):
        task = document.Task(**kwargs)
        task.store(self.db)
        return task

    def update_task(self, task):
        task.store(self.db)
