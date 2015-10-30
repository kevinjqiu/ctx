import datetime

import couchdb

from ctx import document, exception


class DocumentManager(object):
    def __init__(self, db):
        self.db = db

    def get_tasks(self):
        return self.db.view('_all_docs', include_docs=True)

    def create_task(self, **kwargs):
        params = {
            'created_at': datetime.datetime.utcnow(),
        }
        params.update(kwargs)
        task = document.Task(**params)
        try:
            task.store(self.db)
        except couchdb.http.ResourceConflict:
            raise exception.DuplicateTaskID()
        else:
            return task

    def update_task(self, task):
        task.store(self.db)
