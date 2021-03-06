import datetime
import logging

import couchdb

from ctx import document, exception, view, transform


log = logging.getLogger(__name__)


class DocumentManager(object):
    def __init__(self, db):
        self.db = db

    def get_task_by_id(self, id):
        try:
            task = document.Task(**self.db[id])
            task._data['_rev'] = self.db[id].rev
        except couchdb.http.ResourceNotFound:
            raise exception.TaskNotFound()
        else:
            return task

    def get_tasks(self):
        return self.db.view(view.GetTasks.uri(),
                            wrapper=transform.create_task_from_view_result)

    def get_active_task(self):
        result = self.db.view(view.GetActiveTask.uri(),
                              wrapper=transform.create_task_from_view_result)
        if result.total_rows == 0:
            return None
        if result.total_rows > 1:
            raise exception.MultipleActiveTasks()

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
        return task.store(self.db)
