import re
from ctx import document, database
from .base import NeedsDatabase


is_uuid = re.compile(r'[0-9a-f]').search


class TestTask(NeedsDatabase):
    def test_task_with_default_values(self):
        task = document.Task(_id='abc')

        assert task._id == 'abc'
        assert task.is_active is False
        assert task.time_slices == []
        task.store(database.db)

        task = database.db['abc']
        assert task.get('description') is None
        assert task.get('is_active') is False
        assert task.get('time_slices') == []

    def test_task_with_specified_values(self):
        task = document.Task(_id='ABC-123',
                             description='Aye Bee See',
                             is_active=True)
        assert task._id == 'ABC-123'
        assert task.is_active is True
        assert task.description == 'Aye Bee See'
        assert task.time_slices == []
        task.store(database.db)

        task = database.db['ABC-123']
        assert task.get('_id') == 'ABC-123'
        assert task.get('description') == 'Aye Bee See'
        assert task.get('is_active') is True
        assert task.get('time_slices') == []

    def test_task_with_timeslices(self):
        task = document.Task(_id='ABC-123',
                             description='Aye Bee See',
                             is_active=True,
                             time_slices=[document.TimeSlice(note='note')])
        task.store(database.db)
        task = database.db['ABC-123']
        time_slices = task.get('time_slices')
        assert len(time_slices) == 1
        assert time_slices[0].get('note') == 'note'
