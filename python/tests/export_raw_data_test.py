from dataclasses import dataclass, field
from typing_extensions import Literal
from typing import List
import pytest
import os
import os.path
import filecmp
from . import utils

import saleae.automation


@dataclass
class CaptureDesc:
    digital_channels: List[int] = field(default_factory=list)
    analog_channels: List[int] = field(default_factory=list)


capture_desc = {
    'cap1.sal': CaptureDesc(
        digital_channels=[0, 1],
        analog_channels=[0, 1],
    ),
    'cap2.sal': CaptureDesc(
        digital_channels=[2, 3],
    ),
    'cap3.sal': CaptureDesc(
        digital_channels=[4, 5],
        analog_channels=[4],
    ),
}


def get_expected_files(type: Literal['csv', 'bin'], digital_channels: List[int], analog_channels: List[int]):
    """
    Get a list of expected files for export
    """
    expected_files = []
    if type == 'csv':
        if len(analog_channels) > 0:
            expected_files.append('analog.csv')

        if len(digital_channels) > 0:
            expected_files.append('digital.csv')
    else:
        expected_files.extend(f'analog_{ch}.bin' for ch in analog_channels)
        expected_files.extend(f'digital_{ch}.bin' for ch in digital_channels)

    return expected_files


@pytest.mark.parametrize('capture_name', capture_desc.keys())
@pytest.mark.parametrize('type', ['csv', 'bin'])
def test_export(capture_name: str, type: Literal['csv', 'bin'], manager: saleae.automation.Manager, asset_path: str, tmp_path):
    desc = capture_desc[capture_name]

    path = os.path.join(asset_path, f'{capture_name}')

    with manager.load_capture(path) as cap:
        directory = os.path.join(tmp_path, f'export_{capture_name}')

        assert(not os.path.exists(directory))

        if type == 'csv':
            cap.export_raw_data_csv(
                directory=directory,
                analog_channels=desc.analog_channels,
                digital_channels=desc.digital_channels)
        else:
            cap.export_raw_data_binary(
                directory=directory,
                analog_channels=desc.analog_channels,
                digital_channels=desc.digital_channels)

        expected_files = get_expected_files(
            type, desc.digital_channels, desc.analog_channels)

        files_created = os.listdir(directory)
        assert(len(expected_files) == len(files_created))
        for filename in expected_files:
            assert(filename in files_created)


@pytest.mark.parametrize('capture_name', capture_desc.keys())
@pytest.mark.parametrize('type', ['csv', 'bin'])
def test_disabled_channels(capture_name: str, type: Literal['csv', 'bin'], manager: saleae.automation.Manager, asset_path: str, tmp_path):
    desc = capture_desc[capture_name]

    path = os.path.join(asset_path, f'{capture_name}')

    with manager.load_capture(path) as cap:
        directory = os.path.join(tmp_path, f'export_{capture_name}')

        inactive_analog_channels = [ch for ch in range(
            0, 8) if ch not in desc.analog_channels]
        inactive_digital_channels = [ch for ch in range(
            0, 8) if ch not in desc.digital_channels]

        try:
            fn = cap.export_raw_data_csv if type == 'csv' else cap.export_raw_data_binary
            fn(
                directory=directory,
                analog_channels=inactive_analog_channels,
                digital_channels=inactive_digital_channels)

            # We should not get to this point
            assert(False)
        except saleae.automation.InvalidRequestError:
            pass


@pytest.mark.parametrize('type', ['csv', 'bin'])
def test_no_channels(type: Literal['csv', 'bin'], manager: saleae.automation.Manager, asset_path: str, tmp_path):
    capture_name = 'cap1.sal'
    path = os.path.join(asset_path, f'{capture_name}')
    directory = os.path.join(tmp_path, f'export_{capture_name}')

    with manager.load_capture(path) as cap:
        if type == 'csv':
            cap.export_raw_data_csv(
                directory=directory,
                analog_channels=[],
                digital_channels=[])
        else:
            cap.export_raw_data_binary(
                directory=directory,
                analog_channels=[],
                digital_channels=[])

        desc = capture_desc[capture_name]
        expected_files = get_expected_files(
            type, desc.digital_channels, desc.analog_channels)

        files_created = os.listdir(directory)
        assert(len(expected_files) == len(files_created))
        for filename in expected_files:
            assert(filename in files_created)


MIN_DOWNSAMPLE_RATIO = 1
MAX_DOWNSAMPLE_RATIO = 1000000


@pytest.mark.parametrize('analog_downsample_ratio', [MIN_DOWNSAMPLE_RATIO-1, MIN_DOWNSAMPLE_RATIO, MAX_DOWNSAMPLE_RATIO, MAX_DOWNSAMPLE_RATIO+1])
@pytest.mark.parametrize('type', ['csv', 'bin'])
def test_invalid_analog_downsample_ratio(analog_downsample_ratio: int, type: Literal['csv', 'bin'], manager: saleae.automation.Manager, asset_path: str, tmp_path):
    capture_name = 'cap1.sal'
    path = os.path.join(asset_path, capture_name)
    desc = capture_desc[capture_name]

    with manager.load_capture(path) as cap:
        directory = os.path.join(tmp_path, f'export_{capture_name}')

        try:
            if type == 'csv':
                cap.export_raw_data_csv(
                    analog_downsample_ratio=analog_downsample_ratio,
                    directory=directory,
                    analog_channels=desc.analog_channels,
                    digital_channels=desc.digital_channels)
            else:
                cap.export_raw_data_binary(
                    analog_downsample_ratio=analog_downsample_ratio,
                    directory=directory,
                    analog_channels=desc.analog_channels,
                    digital_channels=desc.digital_channels)

            assert(analog_downsample_ratio >=
                   MIN_DOWNSAMPLE_RATIO and analog_downsample_ratio <= MAX_DOWNSAMPLE_RATIO)

        except saleae.automation.InvalidRequestError:
            assert(analog_downsample_ratio <
                   MIN_DOWNSAMPLE_RATIO or analog_downsample_ratio > MAX_DOWNSAMPLE_RATIO)


@dataclass
class ComparisonScenario:
    capture_name: str
    folder: str
    type: Literal['csv', 'bin']
    params: dict


comparison_scenarios = [
    ComparisonScenario(
        capture_name='cap1.sal',
        folder='cap1/all',
        type='csv',
        params=dict(
            analog_downsample_ratio=1,
            analog_channels=[0, 1],
            digital_channels=[0, 1],
        )
    ),
    ComparisonScenario(
        capture_name='cap1.sal',
        folder='cap1/all_isotimestamps',
        type='csv',
        params=dict(
            analog_downsample_ratio=1,
            analog_channels=[0, 1],
            digital_channels=[0, 1],
            iso8601_timestamp=True,
        )
    ),
    ComparisonScenario(
        capture_name='cap1.sal',
        folder='cap1/analog_only',
        type='csv',
        params=dict(
            analog_downsample_ratio=1,
            analog_channels=[0, 1],
            digital_channels=[],
        )
    ),
    ComparisonScenario(
        capture_name='cap1.sal',
        folder='cap1/digital_only',
        type='csv',
        params=dict(
            analog_downsample_ratio=1,
            analog_channels=[],
            digital_channels=[0, 1],
        )
    ),
    ComparisonScenario(
        capture_name='cap1.sal',
        folder='cap1/analog_1_downsample4',
        type='csv',
        params=dict(
            analog_downsample_ratio=4,
            analog_channels=[1],
            digital_channels=[],
        )
    ),
    ComparisonScenario(
        capture_name='cap1.sal',
        folder='cap1/all_bin',
        type='bin',
        params=dict(
            analog_downsample_ratio=1,
            analog_channels=[0, 1],
            digital_channels=[0, 1],
        )
    ),
    ComparisonScenario(
        capture_name='cap1.sal',
        folder='cap1/analog_bin',
        type='bin',
        params=dict(
            analog_downsample_ratio=1,
            analog_channels=[0, 1],
            digital_channels=[],
        )
    ),
    ComparisonScenario(
        capture_name='cap1.sal',
        folder='cap1/digital_bin',
        type='bin',
        params=dict(
            analog_downsample_ratio=1,
            analog_channels=[],
            digital_channels=[0, 1],
        )
    ),
    ComparisonScenario(
        capture_name='cap1.sal',
        folder='cap1/ch1_bin',
        type='bin',
        params=dict(
            analog_downsample_ratio=1,
            analog_channels=[1],
            digital_channels=[1],
        )
    ),
    ComparisonScenario(
        capture_name='cap1.sal',
        folder='cap1/analog_1_downsample4_bin',
        type='bin',
        params=dict(
            analog_downsample_ratio=4,
            analog_channels=[1],
            digital_channels=[],
        )
    ),
]


@pytest.mark.parametrize('scenario', comparison_scenarios)
def test_compare(scenario: ComparisonScenario, manager: saleae.automation.Manager, asset_path: str, tmp_path):
    capture_path = os.path.join(asset_path, scenario.capture_name)

    export_directory = os.path.join(
        tmp_path, f'export_{scenario.capture_name}')

    with manager.load_capture(capture_path) as cap:
        if scenario.type == 'csv':
            cap.export_raw_data_csv(
                directory=export_directory,
                **scenario.params)
        else:
            cap.export_raw_data_binary(
                directory=export_directory,
                **scenario.params)

    expected_directory = os.path.join(asset_path, scenario.folder)

    expected_files = os.listdir(expected_directory)
    actual_files = os.listdir(export_directory)

    for filename in expected_files:
        assert(filename in actual_files)

    for filename in expected_files:
        actual_filepath = os.path.join(export_directory, filename)
        expected_filepath = os.path.join(expected_directory, filename)

        utils.assert_files_match(actual_filepath, expected_filepath, scenario.type == 'bin')


def test_export_all(manager: saleae.automation.Manager, asset_path: str, tmp_path):
    capture_path = os.path.join(asset_path, 'cap2.sal')

    export_directory = os.path.join(tmp_path, f'export_cap2')

    with manager.load_capture(capture_path) as cap:
        cap.export_raw_data_csv(directory=export_directory)
