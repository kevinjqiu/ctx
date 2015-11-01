from .base import NeedsDatabase
from ctx import cli


def test_version(runner):
    result = runner.invoke(cli.cmd_version)
    assert 'version' in result.output
    assert 'db_url' in result.output


class TestNewTaskCommand(NeedsDatabase):
    def test_create_new_task(self, runner):
        result = runner.invoke(cli.cmd_new, ['ABC'])
        assert result.output == "Created task 'ABC'\n"
