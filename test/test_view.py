from ctx import database, view, document
from .base import NeedsDatabase


class TestGetActiveTask(NeedsDatabase):
    def setup_method(self, method):
        super().setup_method(method)
        view.sync_views(database.db)

    def test_get_active_task(self):
        tasks = [document.Task(_id='a', is_active=False),
                 document.Task(_id='b', is_active=True),
                 document.Task(_id='c', is_active=False),
                 ]
        for task in tasks:
            task.store(database.db)

        result = database.db.view(view.GetActiveTask.uri())
        assert result.total_rows == 1
        assert result.rows[0].id == 'b'
