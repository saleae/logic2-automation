from contextlib import contextmanager
from typing import List, Optional, Union, Dict
from dataclasses import dataclass, field
from enum import Enum
import grpc
import logging
import re

from saleae.grpc import saleae_pb2, saleae_pb2_grpc


logger = logging.getLogger(__name__)


class SaleaeError(Exception):
    """
    The base class for all Saleae exceptions. Do not catch this directly.
    """

    pass


class UnknownError(SaleaeError):
    """
    This indicates that the error message from the Logic 2 software was not understood by the python library.
    This could indicate a version mismatch.
    """

    pass


class InternalServerError(SaleaeError):
    """
    An unexpected error occurred in the Logic 2 software. Please submit these errors to Saleae support.
    """

    pass


class InvalidRequestError(SaleaeError):
    """
    The socket request was invalid. See exception message for details.
    """

    pass


class LoadCaptureFailedError(SaleaeError):
    """
    Error loading a saved capture.
    This could indicate that the file does not exist, or the file was saved with a newer version of the Logic 2 software, or that the file was not a valid saved file.
    Try manually loading the file in the Logic 2 software for more information.
    """

    pass


class ExportError(SaleaeError):
    """
    An error occurred either while exporting raw data, a single protocol analyzer, or the protocol analyzer data table.
    Check the exception message for more details.
    """

    pass


class MissingDeviceError(SaleaeError):
    """
    The device ID supplied to the start_capture function is not currently attached to the system, or it has not been detected by the software.
    For general support for device not detected errors, see this support article:
    https://support.saleae.com/troubleshooting/logic-not-detected
    """

    pass


class CaptureError(SaleaeError):
    """
    The base class for all capture related errors. We recommend all automation applications handle this exception type.
    Capture failures occur rarely, and for a handful of reasons. We recommend logging the exception message for later troubleshooting.
    We do not recommend attempting to access or save captures that end in an error. Instead, we recommend starting a new capture.
    Check the exception message for details.
    """

    pass


class DeviceError(CaptureError):
    """
    This error represents any device related error while capturing. USB communication or bandwidth errors, missing calibration, device disconnection while recording, and more.
    Check the exception message for details.
    """

    pass


class OOMError(CaptureError):
    """
    This exception indicates that the capture was automatically terminated because the capture buffer was filled.
    """

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


grpc_error_code_to_exception_type = {
    saleae_pb2.ERROR_CODE_UNSPECIFIED: UnknownError,
    saleae_pb2.ERROR_CODE_INTERNAL_EXCEPTION: InternalServerError,
    saleae_pb2.ERROR_CODE_INVALID_REQUEST: InvalidRequestError,
    saleae_pb2.ERROR_CODE_LOAD_CAPTURE_FAILED: LoadCaptureFailedError,
    saleae_pb2.ERROR_CODE_EXPORT_FAILED: ExportError,
    saleae_pb2.ERROR_CODE_MISSING_DEVICE: MissingDeviceError,
    saleae_pb2.ERROR_CODE_DEVICE_ERROR: DeviceError,
    saleae_pb2.ERROR_CODE_OOM: OOMError,
}


def grpc_error_msg_to_exception(msg: str):
    match = error_message_re.match(msg)
    if match is None:
        return UnknownError(msg)

    code = int(match.group(1))
    error_msg = match.group(2)

    exc_type = grpc_error_code_to_exception_type.get(code, UnknownError)
    return exc_type(error_msg)


class DeviceType(Enum):
    #: Saleae Logic
    LOGIC = saleae_pb2.DEVICE_TYPE_LOGIC

    #: Saleae Logic 4
    LOGIC_4 = saleae_pb2.DEVICE_TYPE_LOGIC_4

    #: Saleae Logic 8
    LOGIC_8 = saleae_pb2.DEVICE_TYPE_LOGIC_8

    #: Saleae Logic 16
    LOGIC_16 = saleae_pb2.DEVICE_TYPE_LOGIC_16

    #: Saleae Logic Pro 8
    LOGIC_PRO_8 = saleae_pb2.DEVICE_TYPE_LOGIC_PRO_8

    #: Saleae Logic Pro 16
    LOGIC_PRO_16 = saleae_pb2.DEVICE_TYPE_LOGIC_PRO_16


@dataclass
class AnalyzerHandle:
    analyzer_id: int


class DeviceConfiguration:
    pass


@dataclass
class DeviceDesc:
    #: Serial number of the device
    serial_number: str

    #: Device type
    device_type: DeviceType

    #: True if this is a simulation devivce
    is_simulation: bool


@dataclass
class GlitchFilterEntry:
    """Represents the glitch filter specifications for a single digital channel"""

    #: Digital channel index
    channel_index: int
    #: minimum pulse width in seconds. The software will round this to the nearest number of samples.
    pulse_width_seconds: float


@dataclass
class LogicDeviceConfiguration(DeviceConfiguration):
    """
    Represents the capture configuration for one of the following devices:

    * Logic 8
    * Logic Pro 8
    * Logic Pro 16

    This class is used to define the specific device configuration when starting a capture with start_capture
    """

    #: list of enabled analog channels. Example: [0,1]
    enabled_analog_channels: List[int] = field(default_factory=list)
    #: list of enabled digital channels. Example: [0,1]
    enabled_digital_channels: List[int] = field(default_factory=list)
    #: Analog sample rate, Samples per second.
    #: This must match a sample rate visible in the software for the given enabled channels.
    #: Omit this when no analog channels are used.
    analog_sample_rate: Optional[int] = None
    #: Digital sample rate, Samples per second.
    #: This must match a sample rate visible in the software for the given enabled channels.
    #: Omit this when no analog channels are used.
    digital_sample_rate: Optional[int] = None
    #: Voltage threshold
    #: Logic Pro 8 and Logic Pro 16 only
    #: Valid options: 1.2, 1.8, and 3.3.
    #: leave unspecified or 0 for Logic 8.
    digital_threshold_volts: Optional[float] = None

    #: Optionally specify a glitch filter for one or more channels.
    #: Only applies to digital channels.
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
    """Represents a digital channel that must be either high or low while the trigger event (edge or pulse) is active"""

    #: the digital channel index of the required channel
    channel_index: int
    #: The state of the channel (HIGH or LOW)
    state: DigitalTriggerLinkedChannelState


@dataclass
class DigitalTriggerCaptureMode:
    """
    This class represents the Digital Trigger Settings, when using start_capture with a digital trigger.
    Note: When using this mode, the wait() function will wait until the trigger is found and the post-trigger recording length is complete and the capture has ended.
    """

    #: Trigger type is RISING, FALLING, PULSE_HIGH, or PULSE_LOW, from the DigitalTriggerType enumeration.
    trigger_type: DigitalTriggerType

    #: Trigger channel where the trigger type is detected.
    trigger_channel_index: int

    #: Minimum pulse width in seconds. Set to zero for no minimum pulse width.
    #: PULSE_HIGH or PULSE_LOW only
    min_pulse_width_seconds: Optional[float] = None

    #: Maximum pulse width in seconds.
    #: PULSE_HIGH or PULSE_LOW only
    max_pulse_width_seconds: Optional[float] = None

    #: Optional list of channels which must be high or low when the trigger channel encounters the trigger type.
    linked_channels: List[DigitalTriggerLinkedChannel] = field(
        default_factory=list)

    #: Seconds of data at end of capture to keep. If unspecified, all data will be kept.
    trim_data_seconds: Optional[float] = None

    #: Seconds of data to record after triggering
    after_trigger_seconds: Optional[float] = None


@dataclass
class TimedCaptureMode:
    """
    This class represents the capture settings when a simple timer mode is used.
    Note: when using this mode, the wait() function will wait until the specified duration is recorded and the capture has ended.
    """

    #: Stop recording after X seconds
    duration_seconds: float

    #: Seconds of data at end of capture to keep. If unspecified, all data will be kept.
    #: Note, this retains the latest X seconds. If specified, the final recording length will be approximately duration_seconds-trim_data_seconds, retaining the latest data.
    trim_data_seconds: Optional[float] = None


@dataclass
class ManualCaptureMode:
    """
    When this is used, a capture must be triggered/stopped manually.
    Note: use the stop() command to stop the capture. The wait() function will return an error.
    """

    #: Seconds of data at end of capture to keep. If unspecified, all data will be kept.
    trim_data_seconds: Optional[float] = None


CaptureMode = Union[ManualCaptureMode,
                    TimedCaptureMode, DigitalTriggerCaptureMode]


@dataclass
class CaptureConfiguration:
    """
    The top-level capture configuration provided to the start_capture function.
    """

    #: Capture buffer size (in megabytes)
    buffer_size: Optional[int] = None

    capture_mode: CaptureMode = field(default_factory=ManualCaptureMode)
    """ 
    | The capture mode. This can be one of the following:
    | ManualCaptureMode
    |   (Looping mode in the software. Stop this capture with the stop() function)
    | TimedCaptureMode
    |   This will record until the specified duration has been captured. Use the wait() function to block until the capture is complete.
    | DigitalTriggerCaptureMode
    |   This will set the digital trigger and record until the trigger has been found and the post-trigger length has been recorded. Use the wait() function to block until the capture is complete.
    """


class Manager:
    """
    Manager is the main class for interacting with the Logic 2 software.

    Creating a new instance of the Manager class will attempt to connect to a running instance of the Logic 2 software.

    Please review the getting started guide for instructions on preparing the Logic 2 software for API connections.
    """

    def __init__(self, port: int):
        """
        Create an instance of the Manager class, and connect to the Logic 2 software.

        This library currently assumes the Logic 2 software is running on the same machine, and will attempt to connect to 127.0.0.1.
        In the future, we'll add support for supplying an IP address, as well as functions to help launch local copies of the application.

        :param port: Port number. By default, Logic 2 uses port 10430.
        """
        self.channel = grpc.insecure_channel(f"127.0.0.1:{port}")
        self.channel.subscribe(lambda value: logger.info(f"sub {value}"))
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

    def get_devices(self, *, include_simulation_devices: bool = False) -> List[DeviceDesc]:
        """
        Returns a list of connected devices. Use this to find the serial numbers of the attached devices.

        :param include_simulation_devices: If True, the return value will also include simulation devices. This can be useful for testing without a physical device.
        """
        request = saleae_pb2.GetDevicesRequest(include_simulation_devices=include_simulation_devices)
        with error_handler():
            reply: saleae_pb2.GetDevicesReply = self.stub.GetDevices(request)

        devices = []
        for device in reply.devices:
            devices.append(DeviceDesc(
                serial_number=device.serial_number,
                device_type=DeviceType(device.device_type),
                is_simulation=device.is_simulation,
            ))

        return devices

    def start_capture(
        self,
        *,
        device_configuration: DeviceConfiguration,
        device_serial_number: str,
        capture_configuration: Optional[CaptureConfiguration] = None,
    ) -> "Capture":
        """Start a new capture

        All capture settings need to be provided. The existing software settings, like selected device or added analyzers, are ignored.

        Be sure to catch DeviceError exceptions raised by this function, and handle them accordingly. See the error section of the library documentation.

        :param device_configuration: An instance of LogicDeviceConfiguration, complete with enabled channels, sample rates, and more.
        :param device_serial_number: The serial number of device to record with.
        :param capture_configuration: The capture configuration, which selects the capture mode: timer, digital trigger, or manual., defaults to None, indicating manual mode.
        :return: Capture instance class. Be sure to call either wait() or stop() before trying to save, export, or close the capture.
        """
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
            if device_configuration.digital_threshold_volts is not None:
                request.logic_device_configuration.digital_threshold_volts = (
                    device_configuration.digital_threshold_volts
                )
            request.logic_device_configuration.glitch_filters.extend(
                [
                    saleae_pb2.GlitchFilterEntry(
                        channel_index=glitch_filter.channel_index,
                        pulse_width_seconds=glitch_filter.pulse_width_seconds,
                    )
                    for glitch_filter in device_configuration.glitch_filters
                ]
            )
        else:
            raise TypeError("Invalid device configuration type")

        if capture_configuration is not None:
            if capture_configuration.buffer_size:
                request.capture_configuration.buffer_size = (
                    capture_configuration.buffer_size
                )

            if capture_configuration.capture_mode is not None:
                trigger = capture_configuration.capture_mode

                if isinstance(trigger, ManualCaptureMode):
                    request.capture_configuration.manual_capture_mode.CopyFrom(
                        saleae_pb2.ManualCaptureMode(
                            trim_data_seconds=trigger.trim_data_seconds
                        )
                    )

                elif isinstance(trigger, TimedCaptureMode):
                    request.capture_configuration.timed_capture_mode.CopyFrom(
                        saleae_pb2.TimedCaptureMode(
                            duration_seconds=trigger.duration_seconds,
                            trim_data_seconds=trigger.trim_data_seconds,
                        )
                    )

                elif isinstance(trigger, DigitalTriggerCaptureMode):
                    request.capture_configuration.digital_capture_mode.CopyFrom(
                        saleae_pb2.DigitalTriggerCaptureMode(
                            trigger_channel_index=trigger.trigger_channel_index,
                            trigger_type=trigger.trigger_type.value,
                            min_pulse_width_seconds=trigger.min_pulse_width_seconds,
                            max_pulse_width_seconds=trigger.max_pulse_width_seconds,
                            after_trigger_seconds=trigger.after_trigger_seconds,
                            trim_data_seconds=trigger.trim_data_seconds,
                            linked_channels=[
                                saleae_pb2.DigitalTriggerLinkedChannel(
                                    channel_index=linked_channel.channel_index,
                                    state=linked_channel.state.value,
                                )
                                for linked_channel in trigger.linked_channels
                            ],
                        )
                    )
                else:
                    raise TypeError("Unexpected trigger type")

        with error_handler():
            reply: saleae_pb2.StartCaptureReply = self.stub.StartCapture(
                request)

        return Capture(self, reply.capture_info.capture_id)

    def load_capture(self, filepath: str) -> "Capture":
        """
        Load a capture.

        The returned Capture object will be fully loaded (`wait_until_done` not required).

        Raises:
            InvalidFileError

        :return: Capture instance class.
        """
        request = saleae_pb2.LoadCaptureRequest(filepath=filepath)
        with error_handler():
            reply: saleae_pb2.LoadCaptureReply = self.stub.LoadCapture(request)

        return Capture(self, reply.capture_info.capture_id)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class Capture:
    """
    This class represents a single capture in the Logic 2 software.

    This class is returned from start_capture() and from load_capture()

    In the case of start_capture(), the capture is still in the recording state, and wait() or stop() must be called before any other function can be called.

    Be sure to close() when you're finished! Otherwise, they will remain in the application as tabs, and will continue to consume memory in the background.
    """

    def __init__(self, manager: Manager, capture_id: int):
        """
        This class cannot be constructed by the user, and is only returned from the Manager class.
        """
        self.manager = manager
        self.capture_id = capture_id

    def add_analyzer(
        self,
        name: str,
        *,
        label: Optional[str] = None,
        settings: Optional[Dict[str, Union[str, int, float, bool]]] = None,
    ) -> AnalyzerHandle:
        """Add an analyzer to the capture

        Note: analyzers already added to a loaded_capture cannot be accessed from the API at this time.

        :param name: The name of the Analyzer, as shown in the Logic 2 application add analyzer list. This must match exactly.
        :param label: The user editable display string for the analyzer. This will be shown in the analyzer data table export, defaults to None
        :param settings: All settings for the analyzer. The keys and values here must exactly match the Analyzer settings as shown in the UI, defaults to None
        :return: Returns an AnalyzerHandle, which is used later for exporting analyzer results.
        """
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
                    raise RuntimeError(
                        "Unsupported analyzer setting value type")

                analyzer_settings[key] = v

        request = saleae_pb2.AddAnalyzerRequest(
            capture_id=self.capture_id,
            analyzer_name=name,
            analyzer_label=label,
            settings=analyzer_settings,
        )

        try:
            reply = self.manager.stub.AddAnalyzer(request)
        except grpc.RpcError as exc:
            raise grpc_error_to_exception(exc) from None

        return AnalyzerHandle(analyzer_id=reply.analyzer_id)

    def remove_analyzer(self, analyzer: "AnalyzerHandle"):
        """
        Removes an analyzer from the capture.

        :param analyzer: AnalyzerHandle returned by add_analyzer()
        """
        request = saleae_pb2.RemoveAnalyzerRequest(
            capture_id=self.capture_id, analyzer_id=analyzer.analyzer_id
        )
        self.manager.stub.RemoveAnalyzer(request)

    def save_capture(self, filepath: str):
        """
        Saves the capture to a .sal file, which can be loaded later either through the UI or with the load_capture() function.

        :param filepath: path to the .sal file. Can be absolute, or relative to the Logic 2 software current working directory.
        """
        request = saleae_pb2.SaveCaptureRequest(
            capture_id=self.capture_id, filepath=filepath
        )
        try:
            reply = self.manager.stub.SaveCapture(request)
        except grpc.RpcError as exc:
            raise grpc_error_to_exception(exc) from None

    def export_analyzer_legacy(
        self, filepath: str, analyzer: AnalyzerHandle, radix: RadixType
    ):
        """
        Exports the specified analyzer using the analyzer plugin export format, and not the data table format.

        Use the export_data_table() function to export analyzer results from the data table.

        :param filepath: file name and path to export to. Should include the file name and extension, typically .csv or .txt.
        :param analyzer: AnalyzerHandle returned from add_analyzer()
        :param radix: Display Radix, from the RadixType enumeration.
        """
        request = saleae_pb2.ExportAnalyzerLegacyRequest(
            capture_id=self.capture_id,
            filepath=filepath,
            analyzer_id=analyzer.analyzer_id,
            radix_type=radix.value,
        )

        try:
            reply = self.manager.stub.ExportAnalyzerLegacy(request)
        except grpc.RpcError as exc:
            raise grpc_error_to_exception(exc) from None

    def export_data_table(
        self,
        filepath: str,
        analyzers: List["AnalyzerHandle"],
        *,
        radix: RadixType,
        iso8601: bool = False,
    ):
        """
        Exports the Analyzer Data Table

        We will be adding more options to this in the future, including the query string, specific columns, specific query columns, and more.

        :param filepath: The specified output file, including extension, .csv.
        :param analyzers: A list of AnalyzerHandles that should be included in the export, returned from add_analyzer()
        :param radix: Display Radix, from the RadixType enumeration. Currently applies to all Analyzers in the export.
        :param iso8601: Use this to output wall clock timestamps, instead of capture relative timestamps. Defaults to False.
        """
        request = saleae_pb2.ExportDataTableRequest(
            capture_id=self.capture_id,
            filepath=filepath,
            analyzer_ids=[h.analyzer_id for h in analyzers],
            iso8601=iso8601,
            radix_type=radix.value,
        )

        with error_handler():
            reply = self.manager.stub.ExportDataTable(request)

    def export_raw_data_csv(
        self,
        directory: str,
        *,
        analog_channels: Optional[List[int]] = None,
        digital_channels: Optional[List[int]] = None,
        analog_downsample_ratio: int = 1,
        iso8601: bool = False,
    ):
        """Exports raw data to CSV file(s)

        This produces exactly the same format as used in the Logic 2 software when using the "Export Raw Data" dialog with the "CSV" option selected.

        Note, the directory parameter is a specific folder that must already exist, and should not include a filename.

        The export system will produce an analog.csv and/or digital.csv file(s) in that directory.

        All selected analog channels will be combined into the analog.csv file, and likewise for digital channels and digital.csv

        If no channels are specified, all channels will be exported.

        :param directory: directory path (not including a filename) to where analog.csv and/or digital.csv will be saved.
        :param analog_channels: list of analog channels to export, defaults to None
        :param digital_channels: list of digital channels to export, defaults to None
        :param analog_downsample_ratio: optional analog downsample ratio, useful to help reduce export file sizes where extra analog resolution isn't needed, defaults to 1
        :param iso8601: Use this to output wall clock timestamps, instead of capture relative timestamps. Defaults to False.
        """
        channels = []
        if analog_channels:
            channels.extend(
                [
                    saleae_pb2.ChannelIdentifier(
                        type=saleae_pb2.CHANNEL_TYPE_ANALOG, index=ch
                    )
                    for ch in analog_channels
                ]
            )
        if digital_channels:
            channels.extend(
                [
                    saleae_pb2.ChannelIdentifier(
                        type=saleae_pb2.CHANNEL_TYPE_DIGITAL, index=ch
                    )
                    for ch in digital_channels
                ]
            )

        request = saleae_pb2.ExportRawDataCsvRequest(
            capture_id=self.capture_id,
            directory=directory,
            channels=channels,
            analog_downsample_ratio=analog_downsample_ratio,
            iso8601=iso8601,
        )

        with error_handler():
            self.manager.stub.ExportRawDataCsv(request)

    def export_raw_data_binary(
        self,
        directory: str,
        *,
        analog_channels: Optional[List[int]] = None,
        digital_channels: Optional[List[int]] = None,
        analog_downsample_ratio: int = 1,
    ):
        """
        Exports raw data to binary files

        This produces exactly the same format as used in the Logic 2 software when using the "Export Raw Data" dialog with the "binary" option selected.

        Documentation for the format can be found here: https://support.saleae.com/faq/technical-faq/binary-export-format-logic-2

        Note, the directory parameter is a specific folder that must already exist, and should not include a filename.

        The export system will produce one .bin file for each channel exported.

        If no channels are specified, all channels will be exported.

        :param directory: directory path (not including a filename) to where .bin files will be saved
        :param analog_channels: list of analog channels to export, defaults to None
        :param digital_channels: list of digital channels to export, defaults to None
        :param analog_downsample_ratio: optional analog downsample ratio, useful to help reduce export file sizes where extra analog resolution isn't needed, defaults to 1
        """
        channels = []
        if analog_channels:
            channels.extend(
                [
                    saleae_pb2.ChannelIdentifier(
                        type=saleae_pb2.CHANNEL_TYPE_ANALOG, index=ch
                    )
                    for ch in analog_channels
                ]
            )
        if digital_channels:
            channels.extend(
                [
                    saleae_pb2.ChannelIdentifier(
                        type=saleae_pb2.CHANNEL_TYPE_DIGITAL, index=ch
                    )
                    for ch in digital_channels
                ]
            )

        request = saleae_pb2.ExportRawDataBinaryRequest(
            capture_id=self.capture_id,
            directory=directory,
            channels=channels,
            analog_downsample_ratio=analog_downsample_ratio,
        )

        with error_handler():
            self.manager.stub.ExportRawDataBinary(request)

    def close(self):
        """
        Closes the capture. Once called, do not use this instance.
        """
        request = saleae_pb2.CloseCaptureRequest(capture_id=self.capture_id)
        with error_handler():
            self.manager.stub.CloseCapture(request)

    def stop(self):
        """
        Stops the capture. Can be used with any capture mode, but this is recommended for use with ManualCaptureMode.

        stop() and wait() should never both be used for a single capture.

        Do not call stop() more than once.

        stop() should never be called for loaded captures.

        If an error occurred during the capture (for example, a USB read timeout, or an out of memory error) that error will be raised by this function.

        Be sure to catch DeviceError exceptions raised by this function, and handle them accordingly. See the error section of the library documentation.
        """
        request = saleae_pb2.StopCaptureRequest(capture_id=self.capture_id)
        with error_handler():
            self.manager.stub.StopCapture(request)

    def wait(self):
        """
        Waits for the capture to complete. This should only be used with TimedCaptureMode or DigitalTriggerCaptureMode.

        for TimedCaptureMode, this will wait for the capture duration to complete.

        For DigitalTriggerCaptureMode, this will wait for the digital trigger to be found and the capture to complete.

        stop() and wait() should never both be used for a single capture.

        Do not call wait() more than once.

        wait() should never be called for loaded captures.

        Be sure to catch DeviceError exceptions raised by this function, and handle them accordingly. See the error section of the library documentation.
        """
        request = saleae_pb2.WaitCaptureRequest(capture_id=self.capture_id)
        with error_handler():
            self.manager.stub.WaitCapture(request)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
