import datetime
import re

import freezegun

from ctx import document, database
from .base import NeedsDatabase


is_uuid = re.compile(r'[0-9a-f]').search


class TestDuration():
    def test_no_duration(self):
        assert '0m' == str(document.Duration(datetime.timedelta()))
        assert '0m' == str(document.Duration(datetime.timedelta(0)))

    def test_with_days(self):
        assert '1d' == str(document.Duration(datetime.timedelta(days=1)))

    def test_with_days_and_minutes(self):
        assert '1d1h' == str(document.Duration(datetime.timedelta(days=1, minutes=60)))

    def test_with_days_and_hours_and_minutes(self):
        assert '1d1h1m' == str(document.Duration(datetime.timedelta(days=1, minutes=61)))

    def test_no_days(self):
        assert '1h1m' == str(document.Duration(datetime.timedelta(hours=1, minutes=1)))
        assert '1h1m' == str(document.Duration(datetime.timedelta(minutes=61)))


class TestTask(NeedsDatabase):
    def test_task_with_default_values(self):
        task = document.Task(_id='abc')

        assert task._id == 'abc'
        assert task.is_active is False
        assert task.time_slices == []
        task.store(database.db)

        task = database.db['abc']
        assert task.get('description') == ''
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
        time_slices = task.time_slices
        assert len(time_slices) == 1
        assert time_slices[0].get('note') == 'note'
        assert time_slices[0].start_time is None
        assert time_slices[0].end_time is None

    def test_task_set_active___no_previous_timeslice(self):
        task = document.Task(_id='ABC-123',
                             description='Aye Bee See',
                             is_active=False)
        with freezegun.freeze_time('2015-10-28 10:00:00'):
            task.set_active(True)
        assert len(task.time_slices) == 1
        assert task.time_slices[0].start_time == datetime.datetime(2015, 10, 28, 10, 0, 0)
        assert task.time_slices[0].end_time is None

    def test_task_set_active___with_previous_timeslice(self):
        task = document.Task(_id='ABC-123',
                             description='Aye Bee See',
                             is_active=False,
                             time_slices=[document.TimeSlice(start_time=datetime.datetime(2015, 10, 28, 9, 0, 0),
                                                             end_time=datetime.datetime(2015, 10, 28, 10, 0, 0))])
        with freezegun.freeze_time('2015-10-28 12:00:00'):
            task.set_active(True)
        assert len(task.time_slices) == 2
        assert task.time_slices[-1].start_time == datetime.datetime(2015, 10, 28, 12, 0, 0)
        assert task.time_slices[-1].end_time is None

    def test_task_set_inactive___no_previous_timeslice(self):
        task = document.Task(_id='ABC-123',
                             description='Aye Bee See',
                             is_active=True)
        with freezegun.freeze_time('2015-10-28 10:00:00'):
            task.set_active(False)
        assert len(task.time_slices) == 0

    def test_task_set_inactive___with_previous_timeslice(self):
        task = document.Task(_id='ABC-123',
                             description='Aye Bee See',
                             is_active=True,
                             time_slices=[document.TimeSlice(start_time=datetime.datetime(2015, 10, 28, 9, 0, 0),
                                                             end_time=None)])
        with freezegun.freeze_time('2015-10-28 12:00:00'):
            task.set_active(False)
        assert len(task.time_slices) == 1
        assert task.time_slices[-1].end_time == datetime.datetime(2015, 10, 28, 12, 0, 0)

    def test_task_total_time___no_time_slices(self):
        task = document.Task(_id='a', time_slices=[])
        assert task.total_time == datetime.timedelta(0)
        assert str(task.total_time) == '0m'

    def test_task_total_time___inactive_task___one_slice(self):
        task = document.Task(
            _id='a',
            is_active=False,
            time_slices=[
                document.TimeSlice(
                    start_time=datetime.datetime(2015, 8, 1, 10, 0, 0),
                    end_time=datetime.datetime(2015, 8, 1, 10, 30, 0),
                )])
        assert task.total_time == datetime.timedelta(minutes=30)
        assert str(task.total_time) == '30m'

    def test_task_total_time___inactive_task___multiple_slices(self):
        task = document.Task(
            _id='a',
            is_active=False,
            time_slices=[
                document.TimeSlice(
                    start_time=datetime.datetime(2015, 8, 1, 10, 0, 0),
                    end_time=datetime.datetime(2015, 8, 1, 10, 30, 0),
                ),
                document.TimeSlice(
                    start_time=datetime.datetime(2015, 8, 2, 10, 0, 0),
                    end_time=datetime.datetime(2015, 8, 2, 11, 0, 0),
                ),
            ])
        assert task.total_time == datetime.timedelta(hours=1, minutes=30)
        assert str(task.total_time) == '1h30m'

    def test_task_total_time___active_task___one_slice(self):
        task = document.Task(
            _id='a',
            is_active=True,
            time_slices=[
                document.TimeSlice(
                    start_time=datetime.datetime(2015, 8, 1, 10, 0, 0),
                )])
        with freezegun.freeze_time('2015-08-03T10:30:00Z'):
            assert task.total_time == datetime.timedelta(days=2, minutes=30)
            assert str(task.total_time) == '2d30m'

    def test_task_total_time___active_task___multiple_slices(self):
        task = document.Task(
            _id='a',
            is_active=True,
            time_slices=[
                document.TimeSlice(
                    start_time=datetime.datetime(2015, 8, 1, 10, 0, 0),
                    end_time=datetime.datetime(2015, 8, 1, 10, 30, 0),
                ),
                document.TimeSlice(
                    start_time=datetime.datetime(2015, 8, 2, 10, 0, 0),
                ),
            ])
        with freezegun.freeze_time('2015-08-02T10:30:00Z'):
            assert task.total_time == datetime.timedelta(minutes=60)

    def test_task_status___no_time_slice(self):
        task = document.Task(
            _id='a',
            is_active=True,
        )
        assert task.status == document.TaskStatus.not_started

    def test_task_status___running(self):
        task = document.Task(
            _id='a',
            is_active=True,
            time_slices=[
                document.TimeSlice(
                    start_time=datetime.datetime(2015, 8, 1, 10, 0, 0),
                    end_time=datetime.datetime(2015, 8, 1, 10, 30, 0),
                ),
                document.TimeSlice(
                    start_time=datetime.datetime(2015, 8, 2, 10, 0, 0),
                ),
            ])
        assert task.status == document.TaskStatus.running

    def test_task_status___paused(self):
        task = document.Task(
            _id='a',
            is_active=True,
            time_slices=[
                document.TimeSlice(
                    start_time=datetime.datetime(2015, 8, 1, 10, 0, 0),
                    end_time=datetime.datetime(2015, 8, 1, 10, 30, 0),
                ),
                document.TimeSlice(
                    start_time=datetime.datetime(2015, 8, 2, 10, 0, 0),
                    end_time=datetime.datetime(2015, 8, 2, 11, 0, 0),
                ),
            ])
        assert task.status == document.TaskStatus.stopped
