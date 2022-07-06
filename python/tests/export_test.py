from dataclasses import dataclass, field
from enum import auto
import time
from typing import Literal
import pytest
import os
import os.path
import pathlib

from saleae import automation

@dataclass
class CaptureDesc:
    digital_channels: list[int] = field(default_factory=list)
    analog_channels: list[int] = field(default_factory=list)

capture_desc = {
    'cap1.sal': CaptureDesc(
        digital_channels=[0,1],
        analog_channels=[0,1],
    ),
    'cap2.sal': CaptureDesc(
        digital_channels=[2,3],
    ),
    'cap3.sal': CaptureDesc(
        digital_channels=[4,5],
        analog_channels=[4],
    ),
}

def get_expected_files(type: Literal['csv', 'bin'], digital_channels: list[int], analog_channels: list[int]):
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
def test_export(capture_name: str, type: Literal['csv', 'bin'], manager: automation.Manager, asset_path: str, tmp_path):
    desc  = capture_desc[capture_name]

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

        expected_files = get_expected_files(type, desc.digital_channels, desc.analog_channels)

        files_created = os.listdir(directory)
        assert(len(expected_files) == len(files_created))
        for filename in expected_files:
            assert(filename in files_created)


@pytest.mark.parametrize('capture_name', capture_desc.keys())
@pytest.mark.parametrize('type', ['csv', 'bin'])
def test_disabled_channels(capture_name: str, type: Literal['csv', 'bin'], manager: automation.Manager, asset_path: str, tmp_path):
    desc  = capture_desc[capture_name]

    path = os.path.join(asset_path, f'{capture_name}')

    with manager.load_capture(path) as cap:
        directory = os.path.join(tmp_path, f'export_{capture_name}')

        inactive_analog_channels = [ch for ch in range(0, 8) if ch not in desc.analog_channels]
        inactive_digital_channels = [ch for ch in range(0, 8) if ch not in desc.digital_channels]

        try:
            fn = cap.export_raw_data_csv if type == 'csv' else cap.export_raw_data_binary
            fn(
                directory=directory,
                analog_channels=inactive_analog_channels,
                digital_channels=inactive_digital_channels)

            # We should not get to this point
            assert(False)
        except automation.InvalidRequest:
            pass


@pytest.mark.parametrize('type', ['csv', 'bin'])
def test_no_channels(type: Literal['csv', 'bin'], manager: automation.Manager, asset_path: str, tmp_path):
    capture_name = 'cap1.sal'
    path = os.path.join(asset_path, f'{capture_name}')
    directory = os.path.join(tmp_path, f'export_{capture_name}')

    with manager.load_capture(path) as cap:
        try:
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

            # We should not get to this point
            assert(False)
        except automation.InvalidRequest:
            pass


MIN_DOWNSAMPLE_RATIO = 1
MAX_DOWNSAMPLE_RATIO = 1000000
@pytest.mark.parametrize('analog_downsample_ratio', [MIN_DOWNSAMPLE_RATIO-1, MIN_DOWNSAMPLE_RATIO, MAX_DOWNSAMPLE_RATIO, MAX_DOWNSAMPLE_RATIO+1])
@pytest.mark.parametrize('type', ['csv', 'bin'])
def test_invalid_analog_downsample_ratio(analog_downsample_ratio: int, type: Literal['csv', 'bin'], manager: automation.Manager, asset_path: str, tmp_path):
    capture_name = 'cap1.sal'
    path = os.path.join(asset_path, capture_name)
    desc  = capture_desc[capture_name]

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

            assert(analog_downsample_ratio >= MIN_DOWNSAMPLE_RATIO and analog_downsample_ratio <= MAX_DOWNSAMPLE_RATIO)

        except automation.InvalidRequest:
            assert(analog_downsample_ratio < MIN_DOWNSAMPLE_RATIO or analog_downsample_ratio > MAX_DOWNSAMPLE_RATIO)