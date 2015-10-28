from ctx.server.app import create_app
from ctx.server import document, db


class TestTask(object):
    @classmethod
    def setup_class(cls):
        cls.app = create_app()
        cls.server = db.server

    def setup_method(self, method):
        for id in db.db:
            del db.db[id]

    def test_task_with_default_values(self):
        task = document.Task()
        a = db.db.save(task.unwrap())

        assert task.title == ''
        assert task.is_active is False
        assert task.time_slices == []

        task = db.db[task.unwrap()['_id']]
        assert task.get('title') == ''
        assert task.get('is_active') is False
        assert task.get('time_slices') == []
