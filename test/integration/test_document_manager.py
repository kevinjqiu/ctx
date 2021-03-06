import pytest
from ctx import document, document_manager, database, exception
from .base import NeedsDatabase


class TestDocumentManager(NeedsDatabase):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.document_manager = document_manager.DocumentManager(database.db)

    def test_get_all_tasks(self):
        t1 = document.Task(_id='a', is_active=True)
        t2 = document.Task(_id='b', is_active=False)
        t3 = document.Task(_id='c', is_active=False,
                           time_slices=[
                               document.TimeSlice(note='foo'),
                           ])

        t1.store(database.db)
        t2.store(database.db)
        t3.store(database.db)

        result = self.document_manager.get_tasks()
        assert len(result) == 3
        assert result.rows[0].id == t1._id
        assert result.rows[1].id == t2._id
        assert result.rows[2].id == t3._id

        assert len(result.rows[2].time_slices) == 1
        assert result.rows[2].time_slices[0].note == 'foo'

    def test_create_new_task(self):
        t = self.document_manager.create_task(_id='a')
        result = self.document_manager.get_tasks()
        assert len(result) == 1
        assert result.rows[0].id == t._id

    def test_create_new_task___duplicate_task_id(self):
        self.document_manager.create_task(_id='a')
        with pytest.raises(exception.DuplicateTaskID):
            self.document_manager.create_task(_id='a')

    def test_update_task(self):
        t = self.document_manager.create_task(_id='a', is_active=True)
        t.is_active = False
        self.document_manager.update_task(t)

        result = self.document_manager.get_tasks()
        assert len(result) == 1
        assert result.rows[0].id == 'a'
        assert result.rows[0].is_active is False

    def test_get_active_task(self):
        for task in [document.Task(_id='a', is_active=True),
                     document.Task(_id='b', is_active=False),
                     document.Task(_id='c', is_active=False)]:
            task.store(database.db)
        task = self.document_manager.get_active_task()
        assert task.id == 'a'

    def test_get_active_task___no_active_task(self):
        for task in [document.Task(_id='a', is_active=False),
                     document.Task(_id='b', is_active=False),
                     document.Task(_id='c', is_active=False)]:
            task.store(database.db)
        task = self.document_manager.get_active_task()
        assert task is None

    def test_get_active_task___too_many_active_tasks(self):
        for task in [document.Task(_id='a', is_active=True),
                     document.Task(_id='b', is_active=True),
                     document.Task(_id='c', is_active=False)]:
            task.store(database.db)
        with pytest.raises(exception.MultipleActiveTasks):
            task = self.document_manager.get_active_task()

    def test_get_task_by_id(self):
        for task in [document.Task(_id='a', is_active=True),
                     document.Task(_id='c', is_active=False)]:
            task.store(database.db)
        task = self.document_manager.get_task_by_id('a')
        assert task.id == 'a'

    def test_get_task_by_id___task_not_exists(self):
        with pytest.raises(exception.TaskNotFound):
            self.document_manager.get_task_by_id('a')
