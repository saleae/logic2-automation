import pytest
import pathlib
import os.path

import saleae.automation

def pytest_addoption(parser):
    parser.addoption('--use-existing', action='store_true')

@pytest.fixture
def asset_path() -> str:
    base_path = pathlib.Path(__file__).parent.resolve()
    return os.path.join(base_path, 'assets')

@pytest.fixture(scope='session')
def manager(request):
    if request.config.getoption('--use-existing'):
        with saleae.automation.Manager(port=10430) as mgr:
            yield mgr
    else:
        with saleae.automation.Manager.launch() as mgr:
            yield mgr
