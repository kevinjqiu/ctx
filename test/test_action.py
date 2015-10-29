from .base import NeedsDatabase
from ctx import database, action, document_manager


class TestNewTask(NeedsDatabase):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.document_manager = document_manager.DocumentManager(database.db)

    def test_create_new_task(self):
        task = action.new_task(self.document_manager, 'ABC', '')
        assert task.is_active is True
