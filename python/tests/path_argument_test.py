from pathlib import Path
from types import SimpleNamespace

import pytest

import saleae.automation
from saleae.automation import AnalyzerHandle, Capture, RadixType


class RecordingStub:
    """Records each request instead of sending it, so these tests don't need Logic 2 running."""

    def __init__(self):
        self.requests = []

    def __getattr__(self, name):
        def call(request):
            self.requests.append(request)
            return SimpleNamespace(capture_info=SimpleNamespace(capture_id=1), analyzer_id=1)
        return call


@pytest.fixture
def stub():
    return RecordingStub()


@pytest.fixture
def capture(stub):
    return Capture(SimpleNamespace(stub=stub), capture_id=1)


analyzer = AnalyzerHandle(analyzer_id=1)

calls = {
    'save_capture': lambda cap, p: cap.save_capture(p),
    'legacy_export_analyzer': lambda cap, p: cap.legacy_export_analyzer(p, analyzer, RadixType.HEXADECIMAL),
    'export_data_table': lambda cap, p: cap.export_data_table(p, [analyzer]),
    'export_raw_data_csv': lambda cap, p: cap.export_raw_data_csv(p),
    'export_raw_data_binary': lambda cap, p: cap.export_raw_data_binary(p),
    'add_high_level_analyzer': lambda cap, p: cap.add_high_level_analyzer(p, 'HLA', input_analyzer=analyzer),
}

path_fields = {
    'save_capture': 'filepath',
    'legacy_export_analyzer': 'filepath',
    'export_data_table': 'filepath',
    'export_raw_data_csv': 'directory',
    'export_raw_data_binary': 'directory',
    'add_high_level_analyzer': 'extension_directory',
}


@pytest.mark.parametrize('method', calls.keys())
@pytest.mark.parametrize('path', [Path('/tmp/saleae/out'), '/tmp/saleae/out'])
def test_capture_methods_accept_path(method, path, capture, stub):
    calls[method](capture, path)

    assert getattr(stub.requests[-1], path_fields[method]) == str(path)


@pytest.mark.parametrize('path', [Path('/tmp/saleae/cap.sal'), '/tmp/saleae/cap.sal'])
def test_load_capture_accepts_path(path, stub):
    saleae.automation.Manager.load_capture(SimpleNamespace(stub=stub), path)

    assert stub.requests[-1].filepath == str(path)
