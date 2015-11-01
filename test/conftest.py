from click.testing import CliRunner
from ctx import database, document_manager

import pytest


@pytest.fixture(scope='function')
def runner(request):
    return CliRunner()


@pytest.fixture(scope='function')
def doc_mgr(request):
    database.init()
    return document_manager.DocumentManager(database.db)
