from pytest_bdd import scenario, given, when, then, parsers


@scenario('ctx_new.feature', "'ctx new' will create a new task")
def test_ctx_new():
    pass


@when(parsers.re('I invoke the command "(?P<command>.+)"'))
def invoke_the_command(runner, command):
    pass


@then(parsers.re('I should see "(?P<result>.+)"'))
def assert_command_result(result):
    pass
