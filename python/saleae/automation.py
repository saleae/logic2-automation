from contextlib import contextmanager
from os import PathLike
from typing import List, Optional, Union, Dict
from dataclasses import dataclass, field
from enum import Enum

from saleae.grpc import saleae_pb2, saleae_pb2_grpc

import grpc

import os.path

import logging
import re

logger = logging.getLogger(__name__)

class SaleaeError(Exception):
    pass

class UnknownError(SaleaeError):
    pass

class InternalServerError(SaleaeError):
    pass

class InvalidRequest(SaleaeError):
    pass

class CaptureError(SaleaeError):
    pass
class DeviceError(CaptureError):
    pass

class OOMError(CaptureError):
    pass

class RadixType(Enum):
    BINARY = saleae_pb2.RADIX_TYPE_BINARY
    DECIMAL = saleae_pb2.RADIX_TYPE_DECIMAL
    HEXADECIMAL = saleae_pb2.RADIX_TYPE_HEXADECIMAL
    ASCII = saleae_pb2.RADIX_TYPE_ASCII

@contextmanager
def error_handler():
    try:
        yield
    except grpc.RpcError as exc:
        raise grpc_error_to_exception(exc) from None

error_message_re = re.compile(r"^(\d+): (.*)$")

def grpc_error_to_exception(exc: grpc.RpcError):
    if exc.code() == grpc.StatusCode.ABORTED:
        message = exc.details()
        return grpc_error_msg_to_exception(message)
    else:
        return exc

def grpc_error_msg_to_exception(msg: str):
    code_to_exception_type = {
        saleae_pb2.ERROR_CODE_INTERNAL_EXCEPTION: InternalServerError,
        saleae_pb2.ERROR_CODE_INVALID_REQUEST: InvalidRequest,
        saleae_pb2.ERROR_CODE_DEVICE_ERROR: DeviceError,
        saleae_pb2.ERROR_CODE_OOM: OOMError,
    }

    match = error_message_re.match(msg)
    if match is None:
        return UnknownError(msg)
    
    code = int(match.group(1))
    error_msg = match.group(2)

    exc_type = code_to_exception_type.get(code, UnknownError)
    return exc_type(error_msg)


@dataclass
class AnalyzerHandle:
    analyzer_id: int


class DeviceConfiguration:
    pass


@dataclass
class GlitchFilterEntry:
    channel_index: int
    pulse_width: float


@dataclass
class LogicDeviceConfiguration(DeviceConfiguration):
    enabled_analog_channels: List[int] = field(default_factory=list)
    enabled_digital_channels: List[int] = field(default_factory=list)

    analog_sample_rate: Optional[int] = None
    digital_sample_rate: Optional[int] = None

    digital_threshold: Optional[float] = None

    glitch_filters: List[GlitchFilterEntry] = field(default_factory=list)


class DigitalTriggerType(Enum):
    RISING = saleae_pb2.DIGITAL_TRIGGER_TYPE_RISING
    FALLING = saleae_pb2.DIGITAL_TRIGGER_TYPE_FALLING
    PULSE_HIGH = saleae_pb2.DIGITAL_TRIGGER_TYPE_PULSE_HIGH
    PULSE_LOW = saleae_pb2.DIGITAL_TRIGGER_TYPE_PULSE_LOW


class DigitalTriggerLinkedChannelState(Enum):
    LOW = saleae_pb2.DIGITAL_TRIGGER_LINKED_CHANNEL_STATE_LOW
    HIGH = saleae_pb2.DIGITAL_TRIGGER_LINKED_CHANNEL_STATE_HIGH


@dataclass
class DigitalTriggerLinkedChannel:
    channel_index: int
    state: DigitalTriggerLinkedChannelState


@dataclass
class DigitalTriggerConfiguration:
    trigger_type: DigitalTriggerType

    trigger_channel_index: int

    min_pulse_duration: Optional[float] = None
    max_pulse_duration: Optional[float] = None

    linked_channels: List[DigitalTriggerLinkedChannel] = field(default_factory=list)

    # Seconds of data before trigger to keep
    # What if you only want to keep data starting _after_ the trigger - negative value?
    pre_trigger_buffer: Optional[float] = None

    # Seconds of data to record after triggering
    post_trigger_buffer: Optional[float] = None

@dataclass
class TimerTriggerConfiguration:
    # Trigger after X seconds
    trigger_time: float

    # Seconds of data before trigger to keep. If unspecified, all data will be kept.
    pre_trigger_buffer: Optional[float] = None


@dataclass
class ManualTriggerConfiguration:
    """
    When this is used, a capture must be triggered/stopped manually.
    
    """
    # Seconds of data before trigger to keep
    pre_trigger_buffer: Optional[float] = None


TriggerConfiguration = Union[ManualTriggerConfiguration, TimerTriggerConfiguration, DigitalTriggerConfiguration]

@dataclass
class CaptureSettings:
    # Capture buffer size (in megabytes)
    buffer_size: Optional[int] = None
    trigger: TriggerConfiguration = field(default_factory=ManualTriggerConfiguration)


class Manager:
    def __init__(self, port: int):
        """
        """
        self.channel = grpc.insecure_channel(f'127.0.0.1:{port}')
        self.channel.subscribe(lambda value: logger.info(f'sub {value}'))
        self._stub = saleae_pb2_grpc.ManagerStub(self.channel)

    def close(self):
        """
        Close connection to Saleae backend, and shut it down if it was created by Manager.

        """
        self.channel.close()
        self.channel = None
        self._stub = None

    @property
    def stub(self) -> saleae_pb2_grpc.ManagerStub:
        if self._stub is None:
            raise RuntimeError("Cannot use Manager after it has been closed")
        return self._stub

    def get_devices(self):
        request = saleae_pb2.GetDevicesRequest()
        with error_handler():
            reply: saleae_pb2.GetDevicesReply = self.stub.GetDevices(request)

    def start_capture(
        self,
        *,
        device_configuration: DeviceConfiguration,
        device_serial_number: str,
        capture_settings: Optional[CaptureSettings] = None,
    ) -> "Capture":
        request = saleae_pb2.StartCaptureRequest()
        request.device_serial_number = device_serial_number

        if isinstance(device_configuration, LogicDeviceConfiguration):
            request.logic_device_configuration.enabled_analog_channels[
                :
            ] = device_configuration.enabled_analog_channels
            request.logic_device_configuration.enabled_digital_channels[
                :
            ] = device_configuration.enabled_digital_channels
            if device_configuration.analog_sample_rate is not None:
                request.logic_device_configuration.analog_sample_rate = (
                    device_configuration.analog_sample_rate
                )
            if device_configuration.digital_sample_rate is not None:
                request.logic_device_configuration.digital_sample_rate = (
                    device_configuration.digital_sample_rate
                )
            if device_configuration.digital_threshold is not None:
                request.logic_device_configuration.digital_threshold = (
                    device_configuration.digital_threshold
                )
            request.logic_device_configuration.glitch_filters.extend(
                [
                    saleae_pb2.GlitchFilterEntry(
                        channel_index=glitch_filter.channel_index,
                        pulse_width=glitch_filter.pulse_width,
                    )
                    for glitch_filter in device_configuration.glitch_filters
                ]
            )
        else:
            raise TypeError("Invalid device configuration type")
        
        if capture_settings is not None:
            if capture_settings.buffer_size:
                request.capture_settings.buffer_size = capture_settings.buffer_size

            if capture_settings.trigger is not None:
                trigger = capture_settings.trigger

                if isinstance(trigger, ManualTriggerConfiguration):
                    request.capture_settings.manual_trigger_settings.CopyFrom(saleae_pb2.ManualTriggerSettings(
                        pre_trigger_seconds=trigger.pre_trigger_buffer
                    ))

                elif isinstance(trigger, TimerTriggerConfiguration):
                    request.capture_settings.timed_trigger_settings.CopyFrom(saleae_pb2.TimedTriggerSettings(
                        trigger_seconds=trigger.trigger_time,
                        pre_trigger_seconds=trigger.pre_trigger_buffer,
                    ))

                elif isinstance(trigger, DigitalTriggerConfiguration):
                    request.capture_settings.digital_trigger_settings.CopyFrom(saleae_pb2.DigitalTriggerSettings(
                        trigger_channel_index=trigger.trigger_channel_index,
                        trigger_type=trigger.trigger_type.value,
                        min_pulse_duration=trigger.min_pulse_duration,
                        max_pulse_duration=trigger.max_pulse_duration,
                        pre_trigger_seconds=trigger.pre_trigger_buffer,
                        post_trigger_seconds=trigger.post_trigger_buffer,
                        linked_channels=[
                            saleae_pb2.DigitalTriggerLinkedChannel(
                                channel_index=linked_channel.channel_index,
                                state=linked_channel.state.value,
                            )
                            for linked_channel in trigger.linked_channels
                        ]
                    ))
                else:
                    raise TypeError("Unexpected trigger type")

        with error_handler():
            reply: saleae_pb2.StartCaptureReply = self.stub.StartCapture(request)

        return Capture(self, reply.capture_info.capture_id)

    def load_capture(self, filepath: str) -> 'Capture':
        """
        Load a capture.

        The returned Capture object will be fully loaded (`wait_until_done` not required).

        Raises:
            InvalidFileError

        """
        request = saleae_pb2.LoadCaptureRequest(filepath=filepath)
        with error_handler():
            reply: saleae_pb2.LoadCaptureReply = self.stub.LoadCapture(request)

        return Capture(self, reply.capture_info.capture_id)




class Capture:
    def __init__(self, manager: Manager, capture_id: int):
        self.manager = manager
        self.capture_id = capture_id

    def add_analyzer(self, name: str, *, label: Optional[str]=None, settings: Optional[Dict[str, Union[str, int, float, bool]]]=None):
        analyzer_settings = {}

        if settings is not None:
            for key, value in settings.items():
                if isinstance(value, str):
                    v = saleae_pb2.AnalyzerSettingValue(string_value=value)
                elif isinstance(value, int):
                    v = saleae_pb2.AnalyzerSettingValue(int64_value=value)
                elif isinstance(value, float):
                    v = saleae_pb2.AnalyzerSettingValue(double_value=value)
                elif isinstance(value, bool):
                    v = saleae_pb2.AnalyzerSettingValue(bool_value=value)
                else:
                    raise RuntimeError("Unsupported analyzer setting value type")

                analyzer_settings[key] = v

        request = saleae_pb2.AddAnalyzerRequest(capture_id=self.capture_id, analyzer_name=name, analyzer_label=label, settings=analyzer_settings)

        try:
            reply = self.manager.stub.AddAnalyzer(request)
        except grpc.RpcError as exc:
            raise grpc_error_to_exception(exc) from None

        return AnalyzerHandle(analyzer_id=reply.analyzer_id)

    def remove_analyzer(self, analyzer: 'AnalyzerHandle'):
        request = saleae_pb2.RemoveAnalyzerRequest(capture_id=self.capture_id, analyzer_id=analyzer.analyzer_id)
        self.manager.stub.RemoveAnalyzer(request)

    def save_capture(self, filepath: str):
        request = saleae_pb2.SaveCaptureRequest(filepath=filepath)
        try:
            reply = self.manager.stub.SaveCapture(request)
        except grpc.RpcError as exc:
            raise grpc_error_to_exception(exc) from None

    def export_analyzer_legacy(self, filepath: str, analyzer: AnalyzerHandle, radix: RadixType):
        request = saleae_pb2.ExportAnalyzerLegacyRequest(
            capture_id=self.capture_id,
            filepath=filepath,
            analyzer_id=analyzer.analyzer_id,
            radix_type=radix.value
        )

        try:
            reply = self.manager.stub.ExportAnalyzerLegacy(request)
        except grpc.RpcError as exc:
            raise grpc_error_to_exception(exc) from None

    def export_data_table(self, filepath: str, analyzers: List['AnalyzerHandle'], *, radix: RadixType, iso8601: bool = False):
        request = saleae_pb2.ExportDataTableRequest(
            capture_id=self.capture_id,
            filepath=filepath,
            analyzer_ids=[h.analyzer_id for h in analyzers],
            iso8601=iso8601,
            radix_type=radix.value)

        with error_handler():
            reply = self.manager.stub.ExportDataTable(request)

    def export_raw_data_csv(self, directory: str, *, analog_channels: Optional[List[int]] = None,
                            digital_channels: Optional[List[int]] = None,
                            analog_downsample_ratio: int = 1, iso8601: bool = False):
        channels = []
        if analog_channels:
            channels.extend([saleae_pb2.ChannelIdentifier(type=saleae_pb2.CHANNEL_TYPE_ANALOG, index=ch) for ch in analog_channels])
        if digital_channels:
            channels.extend([saleae_pb2.ChannelIdentifier(type=saleae_pb2.CHANNEL_TYPE_DIGITAL, index=ch) for ch in digital_channels])

        request = saleae_pb2.ExportRawDataCsvRequest(
            capture_id=self.capture_id,
            directory=directory,
            channels=channels,
            analog_downsample_ratio=analog_downsample_ratio,
            iso8601=iso8601
        )

        with error_handler():
            self.manager.stub.ExportRawDataCsv(request)

    def export_raw_data_binary(self, directory: str, *, analog_channels: Optional[List[int]] = None,
                            digital_channels: Optional[List[int]] = None,
                            analog_downsample_ratio: int = 1):
        channels = []
        if analog_channels:
            channels.extend([saleae_pb2.ChannelIdentifier(type=saleae_pb2.CHANNEL_TYPE_ANALOG, index=ch) for ch in analog_channels])
        if digital_channels:
            channels.extend([saleae_pb2.ChannelIdentifier(type=saleae_pb2.CHANNEL_TYPE_DIGITAL, index=ch) for ch in digital_channels])

        request = saleae_pb2.ExportRawDataBinaryRequest(
            capture_id=self.capture_id,
            directory=directory,
            channels=channels,
            analog_downsample_ratio=analog_downsample_ratio,
        )

        with error_handler():
            self.manager.stub.ExportRawDataBinary(request)

    def close(self):
        request = saleae_pb2.CloseCaptureRequest(capture_id=self.capture_id)
        with error_handler():
            self.manager.stub.CloseCapture(request)

    def stop(self):
        request = saleae_pb2.StopCaptureRequest(capture_id=self.capture_id)
        with error_handler():
            self.manager.stub.StopCapture(request)

    def wait(self):
        request = saleae_pb2.WaitCaptureRequest(capture_id=self.capture_id)
        with error_handler():
            self.manager.stub.WaitCapture(request)


    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
