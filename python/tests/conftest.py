import pytest
import pathlib
import os.path

import saleae.automation

def pytest_addoption(parser):
    parser.addoption('--use-existing', action='store_true')
    parser.addoption('--app-path', action='store')

@pytest.fixture
def asset_path() -> str:
    base_path = pathlib.Path(__file__).parent.resolve()
    return os.path.join(base_path, 'assets')

@pytest.fixture(scope='session')
def manager(request):
    app_path = request.config.getoption('--app-path')
    if app_path is not None:
        with saleae.automation.Manager.launch(app_path) as mgr:
            yield mgr
        pass
    elif request.config.getoption('--use-existing'):
        with saleae.automation.Manager.connect(port=10430) as mgr:
            yield mgr
    else:
        with saleae.automation.Manager.launch() as mgr:
            yield mgr
