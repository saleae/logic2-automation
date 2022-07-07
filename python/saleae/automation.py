from os import PathLike
from typing import List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

from saleae.grpc import saleae_pb2
from saleae.grpc import saleae_pb2_grpc

import grpc

import os
import os.path

import logging
import re

from saleae.grpc.saleae_pb2 import AnalyzerSettingValue, ErrorCode

logger = logging.getLogger(__name__)

class UnknownError(Exception):
    pass

class InternalServerError(Exception):
    pass

class InvalidRequest(Exception):
    pass

class RadixType(Enum):
    BINARY = saleae_pb2.BINARY
    DECIMAL = saleae_pb2.DECIMAL
    HEXADECIMAL = saleae_pb2.HEXADECIMAL
    ASCII = saleae_pb2.ASCII


error_message_re = re.compile(r"^(\d+): (.*)$")

def grpc_error_to_exception(exc: grpc.RpcError):
    if exc.code() == grpc.StatusCode.ABORTED:
        message = exc.details()
        return grpc_error_msg_to_exception(message)
    else:
        return exc

def grpc_error_msg_to_exception(msg: str):
    code_to_exception_type = {
        ErrorCode.INTERNAL_EXCEPTION: InternalServerError,
        ErrorCode.INVALID_REQUEST: InvalidRequest,
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
class LogicDeviceConfiguration(DeviceConfiguration):
    enabled_analog_channels: List[int] = field(default_factory=list)
    enabled_digital_channels: List[int] = field(default_factory=list)

    analog_sample_rate: Optional[int] = None
    digital_sample_rate: Optional[int] = None

    digital_threshold: Optional[float] = None

    glitch_filters: "List[GlitchFilterEntry]" = field(default_factory=list)


@dataclass
class GlitchFilterEntry:
    channel_index: int
    pulse_width: float


class CaptureMode(Enum):
    CIRCULAR = saleae_pb2.CaptureMode.CIRCULAR
    STOP_AFTER_TIME = saleae_pb2.CaptureMode.STOP_AFTER_TIME
    STOP_ON_DIGITAL_TRIGGER = saleae_pb2.CaptureMode.STOP_ON_DIGITAL_TRIGGER


@dataclass
class CaptureSettings:
    buffer_size: Optional[int] = None
    """Capture buffer size (in megabytes)"""

    capture_mode: Optional[CaptureMode] = None

    stop_after_time: Optional[float] = None

    trim_time: Optional[float] = None

    digital_trigger: "Optional[DigitalTriggerSettings]" = None


@dataclass
class DigitalTriggerSettings:
    trigger_type: "DigitalTriggerType"

    record_after_trigger_time: float

    trigger_channel_index: int

    min_pulse_duration: Optional[float] = None
    max_pulse_duration: Optional[float] = None

    linked_channels: "List[DigitalTriggerLinkedChannel]" = field(default_factory=list)


class DigitalTriggerType(Enum):
    RISING = saleae_pb2.DigitalTriggerType.RISING
    FALLING = saleae_pb2.DigitalTriggerType.FALLING
    PULSE_HIGH = saleae_pb2.DigitalTriggerType.PULSE_HIGH
    PULSE_LOW = saleae_pb2.DigitalTriggerType.PULSE_LOW


@dataclass
class DigitalTriggerLinkedChannel:
    channel_index: int
    state: "DigitalTriggerLinkedChannelState"


class DigitalTriggerLinkedChannelState(Enum):
    LOW = saleae_pb2.DigitalTriggerLinkedChannelState.LOW
    HIGH = saleae_pb2.DigitalTriggerLinkedChannelState.HIGH



class Manager:
    def __init__(self, port: int):
        """
        """
        self.channel = grpc.insecure_channel(f'127.0.0.1:{port}')
        self.channel.subscribe(lambda value: logger.info(f'sub {value}'))
        self.stub = saleae_pb2_grpc.ManagerStub(self.channel)

    def close(self):
        """
        Close connection to Saleae backend, and shut it down if it was created by Manager.

        """
        self.channel.close()
        self.channel = None
        self.stub = None

    def get_devices(self):
        request = saleae_pb2.GetDevicesRequest()
        reply: saleae_pb2.GetDevicesReply = self.stub.GetDevices(request)

    def start_capture(
        self,
        *,
        device_configuration: DeviceConfiguration,
        device_serial_number: str = None,
        capture_settings: CaptureSettings = None,
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
        
        if capture_settings is None:
            capture_settings = CaptureSettings()

        if capture_settings.buffer_size is not None:
            request.capture_settings.buffer_size = capture_settings.buffer_size
        if capture_settings.capture_mode is not None:
            request.capture_settings.capture_mode = capture_settings.capture_mode.value
        if capture_settings.stop_after_time is not None:
            request.capture_settings.stop_after_time = capture_settings.stop_after_time
        if capture_settings.trim_time is not None:
            request.capture_settings.trim_time = capture_settings.trim_time
        if capture_settings.digital_trigger is not None:
            digital_trigger = request.capture_settings.digital_trigger
            digital_trigger.trigger_type = (
                capture_settings.digital_trigger.trigger_type.value
            )
            digital_trigger.record_after_trigger_time = (
                capture_settings.digital_trigger.record_after_trigger_time
            )
            digital_trigger.trigger_channel_index = (
                capture_settings.digital_trigger.trigger_channel_index
            )
            if capture_settings.digital_trigger.min_pulse_duration is not None:
                digital_trigger.min_pulse_duration = (
                    capture_settings.digital_trigger.min_pulse_duration
                )
            if capture_settings.digital_trigger.max_pulse_duration is not None:
                digital_trigger.max_pulse_duration = (
                    capture_settings.digital_trigger.max_pulse_duration
                )
            digital_trigger.linked_channels.extend(
                [
                    saleae_pb2.DigitalTriggerLinkedChannel(
                        channel_index=linked_channel.channel_index,
                        state=linked_channel.state.value,
                    )
                    for linked_channel in capture_settings.digital_trigger.linked_channels
                ]
            )

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
        reply: saleae_pb2.LoadCaptureReply = self.stub.LoadCapture(request)
        return Capture(self, reply.capture_info.capture_id)




class Capture:
    def __init__(self, manager: Manager, capture_id: int):
        self.manager = manager
        self.capture_id = capture_id

    def add_analyzer(self, name: str, *, label: Optional[str]=None, settings: Optional[dict[str, Union[str, int, float, bool]]]=None):
        analyzer_settings = {}

        if settings is not None:
            for key, value in settings.items():
                if isinstance(value, str):
                    v = AnalyzerSettingValue(string_value=value)
                elif isinstance(value, int):
                    v = AnalyzerSettingValue(int64_value=value)
                elif isinstance(value, float):
                    v = AnalyzerSettingValue(double_value=value)
                elif isinstance(value, bool):
                    v = AnalyzerSettingValue(bool_value=value)
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

    def export_data_table(self, filepath: str, analyzers: List['AnalyzerHandle'], iso8601: bool = False):
        request = saleae_pb2.ExportDataTableRequest(
            capture_id=self.capture_id,
            filepath=filepath,
            analyzer_ids=[h.analyzer_id for h in analyzers],
            iso8601=iso8601)

        try:
            reply = self.manager.stub.ExportDataTable(request)
        except grpc.RpcError as exc:
            raise grpc_error_to_exception(exc) from None

    def export_raw_data_csv(self, directory: str, *, analog_channels: Optional[List[int]] = None,
                            digital_channels: Optional[List[int]] = None,
                            analog_downsample_ratio: int = 1, iso8601: bool = False):
        channels = []
        if analog_channels:
            channels.extend([saleae_pb2.ChannelIdentifier(type=saleae_pb2.ANALOG, index=ch) for ch in analog_channels])
        if digital_channels:
            channels.extend([saleae_pb2.ChannelIdentifier(type=saleae_pb2.DIGITAL, index=ch) for ch in digital_channels])

        request = saleae_pb2.ExportRawDataCsvRequest(
            capture_id=self.capture_id,
            directory=directory,
            channels=channels,
            analog_downsample_ratio=analog_downsample_ratio,
            iso8601=iso8601
        )

        try:
            self.manager.stub.ExportRawDataCsv(request)
        except grpc.RpcError as exc:
            raise grpc_error_to_exception(exc) from None

    def export_raw_data_binary(self, directory: str, *, analog_channels: Optional[List[int]] = None,
                            digital_channels: Optional[List[int]] = None,
                            analog_downsample_ratio: int = 1):
        channels = []
        if analog_channels:
            channels.extend([saleae_pb2.ChannelIdentifier(type=saleae_pb2.ANALOG, index=ch) for ch in analog_channels])
        if digital_channels:
            channels.extend([saleae_pb2.ChannelIdentifier(type=saleae_pb2.DIGITAL, index=ch) for ch in digital_channels])

        request = saleae_pb2.ExportRawDataBinaryRequest(
            capture_id=self.capture_id,
            directory=directory,
            channels=channels,
            analog_downsample_ratio=analog_downsample_ratio,
        )

        try:
            self.manager.stub.ExportRawDataBinary(request)
        except grpc.RpcError as exc:
            raise grpc_error_to_exception(exc) from None

    def close(self):
        request = saleae_pb2.CloseCaptureRequest(capture_id=self.capture_id)
        self.manager.stub.CloseCapture(request)

    def stop(self):
        request = saleae_pb2.StopCaptureRequest(capture_id=self.capture_id)
        self.manager.stub.StopCapture(request)

    def wait(self):
        request = saleae_pb2.WaitCaptureRequest(capture_id=self.capture_id)
        self.manager.stub.WaitCapture(request)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
