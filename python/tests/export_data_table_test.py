import os.path
import filecmp
from dataclasses import dataclass, field
from typing import List, Optional
import pytest
import sys

from . import utils

import saleae.automation as automation


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
        params=dict(iso8601_timestamp=False)
    ),
    Scenario(
        capture_name='small_spi_capture.sal',
        filename='small_spi_capture/data_table_case2.csv',
        params=dict(iso8601_timestamp=True)
    ),
]



@pytest.mark.skipif(sys.platform == 'linux', reason='Currently failing on linux due to unstable data table column ordering')
@pytest.mark.parametrize('scenario', scenarios)
def test_data_table_export_single_analyzer(scenario: Scenario, manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'small_spi_capture.sal')

    with manager.load_capture(path) as cap:
        analyzer = cap.add_analyzer('SPI', label=f'My SPI', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': '8 Bits per Transfer (Standard)'
        })

        export_filepath = os.path.join(tmp_path, 'data_table.csv')

        cap.export_data_table(filepath=export_filepath, analyzers=[analyzer], **scenario.params)
        expected_filepath = os.path.join(asset_path, scenario.filename)
        utils.assert_files_match(export_filepath, expected_filepath)


@pytest.mark.skipif(sys.platform == 'linux', reason='Currently failing on linux due to unstable data table column ordering')
@pytest.mark.parametrize('scenario', scenarios)
def test_data_table_export_multiple_existing_analyzers(scenario: Scenario, manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'small_spi_capture.sal')

    with manager.load_capture(path) as cap:
        analyzer1 = cap.add_analyzer('SPI', label=f'My SPI', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': '7 Bits per Transfer'
        })
        analyzer2 = cap.add_analyzer('SPI', label=f'My SPI', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': '8 Bits per Transfer (Standard)'
        })
        analyzer3 = cap.add_analyzer('SPI', label=f'My SPI', settings={
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
                utils.assert_files_match(expected_filepath, export_filepath)
            else:
                assert not filecmp.cmp(export_filepath, expected_filepath)


@pytest.mark.skipif(sys.platform == 'linux', reason='Currently failing on linux due to unstable data table column ordering')
def test_data_table_export_multiple_analyzers(manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'small_spi_capture.sal')

    with manager.load_capture(path) as cap:
        analyzer1 = cap.add_analyzer('SPI', label=f'My SPI 1', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': '7 Bits per Transfer'
        })
        analyzer2 = cap.add_analyzer('SPI', label=f'My SPI 2', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': '8 Bits per Transfer (Standard)'
        })
        analyzer3 = cap.add_analyzer('SPI', label=f'My SPI 3', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': '9 Bits per Transfer'
        })

        export_filepath = os.path.join(tmp_path, 'data_table.csv')

        cap.export_data_table(filepath=export_filepath, analyzers=[analyzer1, analyzer2, analyzer3])
        expected_filepath = os.path.join(asset_path, 'small_spi_capture', 'data_table_multiple.csv')

        utils.assert_files_match(export_filepath, expected_filepath)


def test_data_table_export_back_to_back(manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'large_async_capture.sal')

    analyzers = []
    with manager.load_capture(path) as cap:
        for ch in range(2):
            analyzer = cap.add_analyzer('Async Serial', label=f'Async {ch + 1}', settings={
                'Input Channel': 0,
                # 'Input Channel': ch,
                'Bit Rate (Bits/s)': 115200,
            })
            analyzers.append(automation.DataTableExportConfiguration(analyzer, automation.RadixType.HEXADECIMAL))

        export_filepath = os.path.join(tmp_path, 'data_table2.csv')

        cap.export_data_table(filepath=export_filepath, analyzers=analyzers)
        expected_filepath = os.path.join(asset_path, 'large_async_capture', '2_analyzers.csv')
        print(export_filepath, expected_filepath)

        utils.assert_files_match(export_filepath, expected_filepath)


def test_data_table_framev1(manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'cap1.sal')

    analyzers = []
    with manager.load_capture(path) as cap:
        analyzer = cap.add_analyzer('SWD', label='SWD Analyzer', settings={
            'SWDIO': 0,
            'SWCLK': 1,
        })
        analyzers.append(automation.DataTableExportConfiguration(analyzer, automation.RadixType.HEXADECIMAL))

        export_filepath = os.path.join(tmp_path, 'framev1_data.csv')

        cap.export_data_table(filepath=export_filepath, analyzers=analyzers)
        expected_filepath = os.path.join(asset_path, 'cap1', 'swd.csv')

        utils.assert_files_match(export_filepath, expected_filepath)


@dataclass
class FilterScenario:
    capture: str

    # File with the expected export data
    expected_filename: str

    # Columns to export
    columns: Optional[List[str]] = None

    radix: automation.RadixType = automation.RadixType.HEXADECIMAL

    filter: Optional[automation.DataTableFilter] = None


framev1_cols_scenarios = [
    FilterScenario('cap1.sal', 'cap1/swd.csv', []),
    FilterScenario('cap1.sal', 'cap1/swd_type_and_value.csv', ['Type', 'value']),
    FilterScenario('cap1.sal', 'cap1/swd_start_only.csv', ['Start']),
    # Should not include 'type' (incorrect capitalization)
    FilterScenario('cap1.sal', 'cap1/swd_start_only.csv', ['type', 'Start']),
]


@ pytest.mark.parametrize('scenario', framev1_cols_scenarios)
def test_data_table_framev1_cols(scenario: FilterScenario, manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, scenario.capture)

    analyzers = []
    with manager.load_capture(path) as cap:
        # Add a second analyzer that won't be exported
        cap.add_analyzer('SWD', label='SWD Analyzer (before)', settings={
            'SWDIO': 0,
            'SWCLK': 1,
        })

        analyzer = cap.add_analyzer('SWD', label='SWD Analyzer', settings={
            'SWDIO': 0,
            'SWCLK': 1,
        })
        analyzers.append(automation.DataTableExportConfiguration(analyzer, scenario.radix))

        # Add a second analyzer that won't be exported
        cap.add_analyzer('SWD', label='SWD Analyzer (after)', settings={
            'SWDIO': 0,
            'SWCLK': 1,
        })

        export_filepath = os.path.join(tmp_path, 'framev1_data.csv')

        cap.export_data_table(filepath=export_filepath, analyzers=analyzers,
                              columns=scenario.columns, filter=scenario.filter)
        expected_filepath = os.path.join(asset_path, scenario.expected_filename)

        utils.assert_files_match(export_filepath, expected_filepath)


async_scenarios = [
    FilterScenario('large_async_capture.sal', 'large_async_capture/search_hex_0x36.csv',
                   radix=automation.RadixType.HEXADECIMAL, filter=automation.DataTableFilter(columns=['data'], query='0x36')),
    FilterScenario('large_async_capture.sal', 'large_async_capture/search_ascii_0x36.csv',
                   radix=automation.RadixType.ASCII, filter=automation.DataTableFilter(columns=['data'], query='0x36')),
    FilterScenario('large_async_capture.sal', 'large_async_capture/search_ascii_7.csv',
                   radix=automation.RadixType.ASCII, filter=automation.DataTableFilter(columns=['data'], query='7')),
]


@ pytest.mark.parametrize('scenario', async_scenarios)
def test_data_table_filtering(scenario: FilterScenario, manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, scenario.capture)

    analyzers = []
    with manager.load_capture(path) as cap:
        cap.add_analyzer('Async Serial', label=f'Async (should not export)', settings={
            'Input Channel': 0,
            'Bit Rate (Bits/s)': 115200,
        })
        analyzer = cap.add_analyzer('Async Serial', label=f'Async Serial', settings={
            'Input Channel': 0,
            'Bit Rate (Bits/s)': 115200,
        })
        cap.add_analyzer('Async Serial', label=f'Async (should not export)', settings={
            'Input Channel': 0,
            'Bit Rate (Bits/s)': 115200,
        })

        analyzers.append(automation.DataTableExportConfiguration(analyzer, scenario.radix))

        export_filepath = os.path.join(tmp_path, 'framev1_data.csv')

        cap.export_data_table(filepath=export_filepath, analyzers=analyzers,
                              columns=scenario.columns, filter=scenario.filter)
        expected_filepath = os.path.join(asset_path, scenario.expected_filename)

        utils.assert_files_match(export_filepath, expected_filepath)
