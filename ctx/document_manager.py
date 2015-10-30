import datetime

import couchdb

from ctx import document, exception, view, transform


class DocumentManager(object):
    def __init__(self, db):
        self.db = db

    def get_tasks(self):
        return self.db.view(view.GetTasks.uri(),
                            wrapper=transform.create_task_from_view_result)

    def get_current_task(self):
        result = self.db.view(view.GetActiveTask.uri(),
                              wrapper=transform.create_task_from_view_result)
        if result.total_rows == 0:
            return None
        assert result.total_rows <= 1
        return result.rows[0]

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
