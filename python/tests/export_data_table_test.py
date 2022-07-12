import os.path
import filecmp
from dataclasses import dataclass
import pytest
import difflib

from saleae import automation

def assert_files_match(expected, actual):
    if filecmp.cmp(expected, actual):
        assert True
        return

    with open(expected) as f:
        expected_data = f.readlines()

    with open(actual) as f:
        actual_data = f.readlines()

    diff = ''.join(difflib.unified_diff(expected_data, actual_data, fromfile=expected, tofile=actual))

    assert False, f'Files ${expected} and ${actual} do not match: ${diff}'


@dataclass
class Scenario:
    # Name of capture to load
    capture_name: str

    # Name of exported file to compare to
    filename: str

    # Params to pass to `export_data_table`
    params: dict


scenarios = [
    Scenario(
        capture_name='small_spi_capture.sal',
        filename='small_spi_capture/data_table_case1.csv',
        params=dict(iso8601=False,radix=automation.RadixType.ASCII)
    ),
    Scenario(
        capture_name='small_spi_capture.sal',
        filename='small_spi_capture/data_table_case2.csv',
        params=dict(iso8601=True,radix=automation.RadixType.ASCII)
    ),
]

@pytest.mark.parametrize('scenario', scenarios)
def test_data_table_export_single_analyzer(scenario: Scenario, manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'small_spi_capture.sal')

    with manager.load_capture(path) as cap:
        analyzer = cap.add_analyzer('SPI',label=f'My SPI', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': '8 Bits per Transfer (Standard)'
        })

        export_filepath = os.path.join(tmp_path, 'data_table.csv')

        cap.export_data_table(filepath=export_filepath, analyzers=[analyzer], **scenario.params)
        expected_filepath = os.path.join(asset_path, scenario.filename)
        assert(filecmp.cmp(export_filepath, expected_filepath))


@pytest.mark.parametrize('scenario', scenarios)
def test_data_table_export_multiple_existing_analyzers(scenario: Scenario, manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'small_spi_capture.sal')

    with manager.load_capture(path) as cap:
        analyzer1 = cap.add_analyzer('SPI',label=f'My SPI', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': '7 Bits per Transfer'
        })
        analyzer2 = cap.add_analyzer('SPI',label=f'My SPI', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': '8 Bits per Transfer (Standard)'
        })
        analyzer3 = cap.add_analyzer('SPI',label=f'My SPI', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': '9 Bits per Transfer'
        })

        export_filepath = os.path.join(tmp_path, 'data_table.csv')

        # Analyzer 2 should match, Analyzers 1 and 3 should not
        for analyzer in [analyzer1, analyzer2, analyzer3]:
            cap.export_data_table(filepath=export_filepath, analyzers=[analyzer], **scenario.params)
            expected_filepath = os.path.join(asset_path, scenario.filename)

            if analyzer == analyzer2:
                assert_files_match(expected_filepath, export_filepath)
            else:
                assert not filecmp.cmp(export_filepath, expected_filepath)



def test_data_table_export_multiple_analyzers(manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'small_spi_capture.sal')

    cap = manager.load_capture(path)
    analyzer1 = cap.add_analyzer('SPI',label=f'My SPI 1', settings={
        'MISO': 4,
        'Clock': 3,
        'Enable': 5,
        'Bits per Transfer': '7 Bits per Transfer'
    })
    analyzer2 = cap.add_analyzer('SPI',label=f'My SPI 2', settings={
        'MISO': 4,
        'Clock': 3,
        'Enable': 5,
        'Bits per Transfer': '8 Bits per Transfer (Standard)'
    })
    analyzer3 = cap.add_analyzer('SPI',label=f'My SPI 3', settings={
        'MISO': 4,
        'Clock': 3,
        'Enable': 5,
        'Bits per Transfer': '9 Bits per Transfer'
    })

    export_filepath = os.path.join(tmp_path, 'data_table.csv')

    cap.export_data_table(filepath=export_filepath, analyzers=[analyzer1, analyzer2, analyzer3],radix=automation.RadixType.ASCII)
    expected_filepath = os.path.join(asset_path, 'small_spi_capture', 'data_table_multiple.csv')

    assert(filecmp.cmp(export_filepath, expected_filepath))

