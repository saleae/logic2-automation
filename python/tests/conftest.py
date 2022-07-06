import pytest
import pathlib
import os.path

from saleae import automation

@pytest.fixture
def asset_path() -> str:
    base_path = pathlib.Path(__file__).parent.resolve()
    return os.path.join(base_path, 'assets')

@pytest.fixture
def manager():
    mgr = automation.Manager(port=50051)
    yield mgr
    mgr.close()
