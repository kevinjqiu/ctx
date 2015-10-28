import pytest
from ctx import document, document_manager, database


database.init()


@pytest.fixture
def task_with_no_slices(active=False):
    return document.Task(is_active=active)


class TestDocumentManager(object):
    @classmethod
    def setup_class(cls):
        cls.document_manager = document_manager.DocumentManager(database.db)

    # TODO: refacctor to DatabaseTestCase
    def setup_method(self, method):
        for id in database.db:
            del database.db[id]

    def test_get_all_tasks(self):
        task_with_no_slices(active=True).store(database.db)
        task_with_no_slices(active=False).store(database.db)
        result = self.document_manager.get_tasks()
