import pytest
from ctx import document, document_manager, database
from .base import NeedsDatabase


class TestDocumentManager(NeedsDatabase):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.document_manager = document_manager.DocumentManager(database.db)

    def test_get_all_tasks(self):
        t1 = document.Task(_id='a', active=True)
        t2 = document.Task(_id='b', active=False)
        t3 = document.Task(_id='c', active=False,
                           time_slices=[
                               document.TimeSlice(note='foo'),
                           ])

        t1.store(database.db)
        t2.store(database.db)
        t3.store(database.db)

        result = self.document_manager.get_tasks()
        assert result.total_rows == 3
        assert result.rows[0].doc.get('_id') == t1._id
        assert result.rows[1].doc.get('_id') == t2._id
        assert result.rows[2].doc.get('_id') == t3._id

        assert len(result.rows[2].doc.get('time_slices')) == 1
        assert result.rows[2].doc.get('time_slices')[0].get('note') == 'foo'

    def test_create_new_task(self):
        t = self.document_manager.create_task(_id='a')
        result = self.document_manager.get_tasks()
        assert result.total_rows == 1
        assert result.rows[0].doc.get('_id') == t._id

    def test_update_task(self):
        t = self.document_manager.create_task(_id='a', is_active=True)
        t.is_active = False
        self.document_manager.update_task(t)

        result = self.document_manager.get_tasks()
        assert result.total_rows == 1
        assert result.rows[0].doc.get('_id') == 'a'
        assert result.rows[0].doc.get('is_active') is False
