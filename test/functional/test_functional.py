import freezegun
from ctx import cli, database, view, document
from pytest_bdd import scenario
from .step import *  # noqa


@scenario('ctx_new.feature', 'duplicate task id')
def test_duplicate_task_id():
    pass


@scenario('ctx_new.feature', 'create a new task')
def test_create_a_new_task():
    pass


@scenario('ctx_new.feature', 'create a new task and switch to it')
def test_create_and_switch_task():
    pass


@scenario('ctx_new.feature', 'create a new task with description')
def test_create_with_description():
    pass
