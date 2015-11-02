import freezegun
from ctx import cli, database, view, document
from pytest_bdd import given, when, then, parsers


SUBCOMMAND_MAP = {
    'new': cli.cmd_new,
}


@given('I have a clean database')
def i_have_a_clean_slate():
    database.init()
    database.server.delete(database.db.name)
    database.init()
    view.sync_views(database.db)


@given(parsers.re('The current time is "(?P<time>.+)"'))
def set_current_time(request, time):
    request.freezed_time = freezegun.freeze_time(time)
    request.freezed_time.__enter__()


@given(parsers.re('I have an active task "(?P<task_id>.+?)"(?: started at "(?P<start_time>.+)")?'))
def create_a_new_task(doc_mgr, task_id, start_time):
    task = doc_mgr.create_task(_id=task_id, is_active=True)
    if start_time:
        task.time_slices.append(document.TimeSlice(start_time=start_time))
        doc_mgr.update_task(task)


@when(parsers.re('I invoke the command "(?P<command>.+)"'))
def invoke_the_command(runner, command):
    tokens = command.split(' ')
    subcommand, args = tokens[1], tokens[2:]

    runner.invoke(SUBCOMMAND_MAP[subcommand], args)


@then(parsers.re('I should see "(?P<result>.+)"'))
def assert_command_result(runner, result):
    assert result.strip() in runner.last_result.output.strip()


@then(parsers.re('The active task is "(?P<task_id>.+)"'))
def assert_current_task(doc_mgr, task_id):
    task = doc_mgr.get_active_task()
    assert task.id == task_id


@then(parsers.re('(?P<task_id>.+) should end at (?P<end_time>.+)'))
def assert_task_end_time(doc_mgr, task_id, end_time):
    task = doc_mgr.get_task_by_id(task_id)
    assert str(task.time_slices[-1].end_time) == end_time


@then(parsers.re('(?P<task_id>.+) should start at (?P<start_time>.+)'))
def assert_task_start_time(doc_mgr, task_id, start_time):
    task = doc_mgr.get_task_by_id(task_id)
    assert str(task.time_slices[-1].start_time) == start_time


@then(parsers.re('(?P<task_id>.+) should have duration "(?P<duration>.+)"'))
def assert_duration(doc_mgr, task_id, duration):
    task = doc_mgr.get_task_by_id(task_id)
    assert str(task.total_time) == duration


@then(parsers.re('(?P<task_id>.+) should have description "(?P<description>.+)"'))
def assert_description(doc_mgr, task_id, description):
    task = doc_mgr.get_task_by_id(task_id)
    assert task.description == description
