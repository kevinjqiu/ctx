from click.testing import CliRunner
from ctx import database, document_manager

import pytest


class StatefulCliRunner(CliRunner):
    def invoke(self, *args, **kwargs):
        self.last_result = super().invoke(*args, **kwargs)
        return self.last_result


@pytest.fixture(scope='function')
def runner(request):
    return StatefulCliRunner()


@pytest.fixture(scope='function')
def doc_mgr(request):
    database.init()
    return document_manager.DocumentManager(database.db)
