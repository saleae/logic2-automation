from typing import Dict, List
import saleae.automation as automation

from dataclasses import dataclass
import os.path
import time
import pytest
from saleae.grpc.saleae_pb2 import DigitalTriggerType

SIMULATION_LOGIC_8 = 'F4243'
SIMULATION_LOGIC_PRO_8 = 'F4244'
SIMULATION_LOGIC_PRO_16 = 'F4241'


def test_start_capture(manager: automation.Manager, tmp_path):
    serial = SIMULATION_LOGIC_PRO_8
    config = automation.LogicDeviceConfiguration(
        enabled_digital_channels=[0, 3, 4, 5],
        digital_sample_rate=500_000_000,
        digital_threshold_volts=3.3,
    )
    trigger = automation.ManualCaptureMode()

    with manager.start_capture(device_id=serial, device_configuration=config) as cap:

        time.sleep(1)

        cap.stop()

        async_analyzer = cap.add_analyzer('Async Serial', settings={
            'Input Channel': 0,
            'Bit Rate (Bits/s)': 115200,
        })
        spi_analyzer = cap.add_analyzer('SPI', label=f'My SPI Analyzer', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': '16 Bits per Transfer'
        })

        cap.export_data_table(
            os.path.join(tmp_path, 'data_table_export.csv'),
            # analyzers=[async_analyzer, spi_analyzer], radix=automation.RadixType.BINARY)
            analyzers=[
                automation.DataTableExportConfiguration(analyzer=async_analyzer, radix=automation.RadixType.BINARY),
                automation.DataTableExportConfiguration(analyzer=spi_analyzer, radix=automation.RadixType.BINARY),
            ])

        time.sleep(3)


trigger_configs = [
    automation.ManualCaptureMode(trim_data_seconds=None),
    automation.ManualCaptureMode(trim_data_seconds=0),
    automation.ManualCaptureMode(trim_data_seconds=0.2),
    automation.ManualCaptureMode(trim_data_seconds=5),

    automation.TimedCaptureMode(duration_seconds=1.0),

    automation.DigitalTriggerCaptureMode(trigger_channel_index=0, trigger_type=automation.DigitalTriggerType.FALLING),
    automation.DigitalTriggerCaptureMode(trigger_channel_index=3, trigger_type=automation.DigitalTriggerType.RISING),
    automation.DigitalTriggerCaptureMode(
        trigger_channel_index=4, trigger_type=automation.DigitalTriggerType.PULSE_LOW, min_pulse_width_seconds=1e-9, max_pulse_width_seconds=0.5),
    automation.DigitalTriggerCaptureMode(
        trigger_channel_index=5, trigger_type=automation.DigitalTriggerType.PULSE_HIGH, min_pulse_width_seconds=1e-9, max_pulse_width_seconds=0.5),

]


@pytest.mark.parametrize('trigger', trigger_configs)
def test_trigger_config(trigger: automation.CaptureMode, manager: automation.Manager):
    serial = SIMULATION_LOGIC_PRO_8
    config = automation.LogicDeviceConfiguration(
        enabled_digital_channels=[0, 3, 4, 5],
        digital_sample_rate=500_000_000,
        digital_threshold_volts=3.3,
    )
    capture_settings = automation.CaptureConfiguration(capture_mode=trigger)

    with manager.start_capture(device_id=serial, device_configuration=config, capture_configuration=capture_settings) as cap:
        if isinstance(trigger, automation.ManualCaptureMode):
            cap.stop()
        else:
            cap.wait()


@dataclass
class ThresholdScenario:
    serial: str
    threshold: float
    valid: bool


threshold_scenarios = [
    ThresholdScenario(serial=SIMULATION_LOGIC_8, threshold=-0.1, valid=False),
    ThresholdScenario(serial=SIMULATION_LOGIC_8, threshold=0.0, valid=True),
    ThresholdScenario(serial=SIMULATION_LOGIC_8, threshold=1.1, valid=False),
    ThresholdScenario(serial=SIMULATION_LOGIC_8, threshold=1.2, valid=False),
    ThresholdScenario(serial=SIMULATION_LOGIC_8, threshold=1.8, valid=False),
    ThresholdScenario(serial=SIMULATION_LOGIC_8, threshold=3.3, valid=False),
    ThresholdScenario(serial=SIMULATION_LOGIC_8, threshold=3.4, valid=False),

    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_8, threshold=-0.1, valid=False),
    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_8, threshold=0.0, valid=True),
    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_8, threshold=1.1, valid=False),
    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_8, threshold=1.2, valid=True),
    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_8, threshold=1.8, valid=True),
    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_8, threshold=3.3, valid=True),
    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_8, threshold=3.4, valid=False),

    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_16, threshold=0.0, valid=True),
    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_16, threshold=1.1, valid=False),
    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_16, threshold=1.2, valid=True),
    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_16, threshold=1.8, valid=True),
    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_16, threshold=3.3, valid=True),
    ThresholdScenario(serial=SIMULATION_LOGIC_PRO_16, threshold=3.4, valid=False),
]


@pytest.mark.parametrize('scenario', threshold_scenarios)
def test_threshold_validation(scenario: ThresholdScenario, manager: automation.Manager):
    serial = scenario.serial
    config = automation.LogicDeviceConfiguration(
        enabled_digital_channels=[0, 3, 4],
        digital_sample_rate=100_000_000,
        digital_threshold_volts=scenario.threshold,
    )

    try:
        with manager.start_capture(device_id=serial, device_configuration=config) as cap:
            cap.stop()
        assert scenario.valid, "Expected failure, digital threshold options not available on Logic 8"
    except automation.SaleaeError as exc:
        assert not scenario.valid, "Failure not expected, digital threshold options should be valid"


@dataclass
class EnabledChannelScenario:
    serial: str
    digital_channels: List[int]
    analog_channels: List[int]
    digital_rate: int
    analog_rate: int
    valid: bool


LOGIC_8_RATES = dict(digital_rate=10_000_000, analog_rate=625_000)
LOGIC_PRO_RATES = dict(digital_rate=6_250_000, analog_rate=781_250)

enabled_channel_scenarios = [
    EnabledChannelScenario(serial=SIMULATION_LOGIC_8, digital_channels=[],
                           analog_channels=[], valid=False, **LOGIC_8_RATES),
    EnabledChannelScenario(serial=SIMULATION_LOGIC_8, digital_channels=[
                           0], analog_channels=[], valid=True, **LOGIC_8_RATES),
    EnabledChannelScenario(serial=SIMULATION_LOGIC_8, digital_channels=[],
                           analog_channels=[0], valid=True, **LOGIC_8_RATES),
    EnabledChannelScenario(serial=SIMULATION_LOGIC_8, digital_channels=[0, 1, 2, 3, 4, 5, 6, 7], analog_channels=[
                           0, 1, 2, 3, 4, 5, 6, 7], valid=True, **LOGIC_8_RATES),

    EnabledChannelScenario(serial=SIMULATION_LOGIC_PRO_8, digital_channels=[],
                           analog_channels=[], valid=False, **LOGIC_PRO_RATES),
    EnabledChannelScenario(serial=SIMULATION_LOGIC_PRO_8, digital_channels=[
                           0], analog_channels=[], valid=True, **LOGIC_PRO_RATES),
    EnabledChannelScenario(serial=SIMULATION_LOGIC_PRO_8, digital_channels=[],
                           analog_channels=[0], valid=True, **LOGIC_PRO_RATES),
    EnabledChannelScenario(serial=SIMULATION_LOGIC_PRO_8, digital_channels=[0, 1, 2, 3, 4, 5, 6, 7], analog_channels=[
                           0, 1, 2, 3, 4, 5, 6, 7], valid=True, **LOGIC_PRO_RATES),

    EnabledChannelScenario(serial=SIMULATION_LOGIC_PRO_16, digital_channels=[],
                           analog_channels=[], valid=False, **LOGIC_PRO_RATES),
    EnabledChannelScenario(serial=SIMULATION_LOGIC_PRO_16, digital_channels=[
                           0], analog_channels=[], valid=True, **LOGIC_PRO_RATES),
    EnabledChannelScenario(serial=SIMULATION_LOGIC_PRO_16, digital_channels=[],
                           analog_channels=[0], valid=True, **LOGIC_PRO_RATES),
    EnabledChannelScenario(serial=SIMULATION_LOGIC_PRO_16, digital_channels=[0, 1, 2, 3, 4, 5, 6, 7], analog_channels=[
                           0, 1, 2, 3, 4, 5, 6, 7], valid=True, **LOGIC_PRO_RATES),
]


@pytest.mark.parametrize('scenario', enabled_channel_scenarios)
def test_channel_validation(scenario: EnabledChannelScenario, manager: automation.Manager, asset_path: str, tmp_path):
    serial = scenario.serial
    config = automation.LogicDeviceConfiguration(
        enabled_digital_channels=scenario.digital_channels,
        enabled_analog_channels=scenario.analog_channels,
        digital_sample_rate=scenario.digital_rate,
        analog_sample_rate=scenario.analog_rate,
    )

    try:
        with manager.start_capture(device_id=serial, device_configuration=config) as cap:
            cap.stop()
        assert scenario.valid, 'Expected failure'
    except automation.SaleaeError as exc:
        assert not scenario.valid, f'Failure not expected: {exc}'


@dataclass
class GlitchFilterScenario:
    serial: str
    channels: List[int]
    glitch_filters: Dict[int, float]
    digital_rate: int
    analog_rate: int
    valid: bool


enabled_channel_scenarios = [
    GlitchFilterScenario(serial=SIMULATION_LOGIC_8, channels=[0], glitch_filters={0: 1}, valid=True, **LOGIC_8_RATES),
    GlitchFilterScenario(serial=SIMULATION_LOGIC_8, channels=[0], glitch_filters={0: 0}, valid=False, **LOGIC_8_RATES),
    GlitchFilterScenario(serial=SIMULATION_LOGIC_8, channels=[0], glitch_filters={0: -1}, valid=False, **LOGIC_8_RATES),
    GlitchFilterScenario(serial=SIMULATION_LOGIC_8, channels=[0], glitch_filters={1: 1}, valid=False, **LOGIC_8_RATES),
    GlitchFilterScenario(serial=SIMULATION_LOGIC_8, channels=[1], glitch_filters={0: 1}, valid=False, **LOGIC_8_RATES),
    GlitchFilterScenario(serial=SIMULATION_LOGIC_8, channels=[
                         0, 1], glitch_filters={0: 1}, valid=True, **LOGIC_8_RATES),
    GlitchFilterScenario(serial=SIMULATION_LOGIC_8, channels=[0, 1], glitch_filters={
                         0: 1, 1: 1}, valid=True, **LOGIC_8_RATES),
]


@pytest.mark.parametrize('scenario', enabled_channel_scenarios)
def test_glitch_filter(scenario: GlitchFilterScenario, manager: automation.Manager, asset_path: str, tmp_path):
    serial = scenario.serial
    config = automation.LogicDeviceConfiguration(
        enabled_digital_channels=scenario.channels,
        digital_sample_rate=scenario.digital_rate,
        glitch_filters=[automation.GlitchFilterEntry(channel_index=key, pulse_width_seconds=value)
                        for key, value in scenario.glitch_filters.items()],
    )

    try:
        with manager.start_capture(device_id=serial, device_configuration=config) as cap:
            cap.stop()
        assert scenario.valid, 'Expected failure'
    except automation.SaleaeError as exc:
        assert not scenario.valid, f'Failure not expected: {exc}'
