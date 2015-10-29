from ctx import document, database
from .base import NeedsDatabase


class TestTask(NeedsDatabase):
    def test_task_with_default_values(self):
        task = document.Task()

        assert task.title == ''
        assert task.is_active is False
        assert task.time_slices == []
        task.store(database.db)

        task = database.db[task.unwrap()['_id']]
        assert task.get('title') == ''
        assert task.get('description') == ''
        assert task.get('is_active') is False
        assert task.get('time_slices') == []

    def test_task_with_specified_values(self):
        task = document.Task(title='ABC-123',
                             description='Aye Bee See',
                             is_active=True)
        assert task.title == 'ABC-123'
        assert task.is_active is True
        assert task.description == 'Aye Bee See'
        assert task.time_slices == []
        task.store(database.db)

        task = database.db[task.unwrap()['_id']]
        assert task.get('title') == 'ABC-123'
        assert task.get('description') == 'Aye Bee See'
        assert task.get('is_active') is True
        assert task.get('time_slices') == []

    def test_task_with_timeslices(self):
        task = document.Task(title='ABC-123',
                             description='Aye Bee See',
                             is_active=True,
                             time_slices=[document.TimeSlice(note='note')])
        task.store(database.db)
        task = database.db[task.unwrap()['_id']]
        time_slices = task.get('time_slices')
        assert len(time_slices) == 1
        assert time_slices[0].get('note') == 'note'
