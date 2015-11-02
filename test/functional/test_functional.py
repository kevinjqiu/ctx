import freezegun
from ctx import cli, database, view, document
from pytest_bdd import scenario
from .step import *  # noqa


@scenario('ctx_new.feature', 'duplicate task id')
def test_new___duplicate_task_id():
    pass


@scenario('ctx_new.feature', 'create a new task')
def test_new():
    pass


@scenario('ctx_new.feature', 'create a new task and switch to it')
def test_new___and_switch_task():
    pass


@scenario('ctx_new.feature', 'create a new task with description')
def test_new___with_description():
    pass


@scenario('ctx_info.feature', 'no current context')
def test_info___no_active_task():
    pass
