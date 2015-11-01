import freezegun
import datetime
from .base import NeedsDatabase
from ctx import cli, document


def test_version(runner):
    result = runner.invoke(cli.cmd_version)
    assert 'version' in result.output
    assert 'db_url' in result.output


class TestNewTaskCommand(NeedsDatabase):
    def test_create_new_task(self, doc_mgr, runner):
        previous_task = document.Task(_id='ABC', is_active=True,
                                      time_slices=[
                                          document.TimeSlice(start_time=datetime.datetime(2015, 10, 10, 9))
                                      ])
        previous_task.store(doc_mgr.db)
        result = runner.invoke(cli.cmd_new, ['DEF'])
        assert result.exception is None
        assert result.output == "Created task 'DEF'\n"
        previous_task = doc_mgr.db['ABC']
        assert previous_task.get('is_active')

    def test_create_new_task___duplicate_task_id(self, doc_mgr, runner):
        previous_task = document.Task(_id='ABC', is_active=True,
                                      time_slices=[
                                          document.TimeSlice(start_time=datetime.datetime(2015, 10, 10, 9))
                                      ])
        previous_task.store(doc_mgr.db)
        result = runner.invoke(cli.cmd_new, ['ABC'])
        assert result.exception is None
        assert result.output == "Cannot create task 'ABC': Duplicate task ID\n"

    @freezegun.freeze_time('2015-10-10T10:10:10Z')
    def test_create_new_task_and_switch(self, doc_mgr, runner):
        result = runner.invoke(cli.cmd_new, ['-s', 'ABC'])
        assert result.output == "Created task 'ABC'\nSwitched to task 'ABC'\n"
        active_task = doc_mgr.get_active_task()
        assert active_task.id == 'ABC'
        assert len(active_task.time_slices) == 1
        assert str(active_task.time_slices[0].start_time) == '2015-10-10 10:10:10'
        assert active_task.time_slices[0].end_time is None

    @freezegun.freeze_time('2015-10-10T10:10:10Z')
    def test_create_new_task_and_switch___with_description(self, doc_mgr, runner):
        result = runner.invoke(cli.cmd_new, ['-d', 'description', '-s', 'ABC'])
        assert result.output == "Created task 'ABC'\nSwitched to task 'ABC'\n"
        active_task = doc_mgr.get_active_task()
        assert active_task.id == 'ABC'
        assert active_task.description == 'description'
        assert len(active_task.time_slices) == 1
        assert str(active_task.time_slices[0].start_time) == '2015-10-10 10:10:10'
        assert active_task.time_slices[0].end_time is None

    @freezegun.freeze_time('2015-10-10T10:10:10Z')
    def test_create_new_task_and_switch___will_stop_the_previously_active_task(self, doc_mgr, runner):
        previous_task = document.Task(_id='ABC', is_active=True,
                                      time_slices=[
                                          document.TimeSlice(start_time=datetime.datetime(2015, 10, 10, 9))
                                      ])
        previous_task.store(doc_mgr.db)

        result = runner.invoke(cli.cmd_new, ['-s', 'DEF'])
        assert result.exception is None
        assert result.output == "Created task 'DEF'\nSwitched to task 'DEF'\n"

        previous_task = doc_mgr.db['ABC']
        assert not previous_task.get('is_active')
        assert str(previous_task.get('time_slices')[-1].get('end_time')) == '2015-10-10T10:10:10Z'

        active_task = doc_mgr.get_active_task()
        assert active_task.id == 'DEF'
        assert len(active_task.time_slices) == 1
        assert str(active_task.time_slices[0].start_time) == '2015-10-10 10:10:10'
        assert active_task.time_slices[0].end_time is None
