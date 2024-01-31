from pathlib import Path
from typing import Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import grpc
import logging
import subprocess
import time

from . import errors

from .capture import Capture

from saleae.grpc import saleae_pb2, saleae_pb2_grpc

logger = logging.getLogger(__name__)

@dataclass
class Version:
    major: int
    minor: int
    patch: int


@dataclass
class AppInfo:
    """Logic 2 Application Information"""
    #: Version of saleae.proto that the server (Logic 2) is using
    api_version: Version

    #: Logic 2 application version
    app_version: str

    #: Logic 2 main application PID
    app_pid: int


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


class DeviceConfiguration:
    pass


@dataclass
class DeviceDesc:
    #: Id of the device
    device_id: str

    #: Device type
    device_type: DeviceType

    #: True if this is a simulation devivce
    is_simulation: bool


@dataclass
class GlitchFilterEntry:
    """Represents the glitch filter specifications for a single digital channel"""

    #: Digital channel index
    channel_index: int
    #: Minimum pulse width in seconds. The software will round this to the nearest number of samples.
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
    #: Rising Edge
    RISING = saleae_pb2.DIGITAL_TRIGGER_TYPE_RISING

    #: Falling Edge
    FALLING = saleae_pb2.DIGITAL_TRIGGER_TYPE_FALLING

    #: High Pulse
    PULSE_HIGH = saleae_pb2.DIGITAL_TRIGGER_TYPE_PULSE_HIGH

    #: Low Pulse
    PULSE_LOW = saleae_pb2.DIGITAL_TRIGGER_TYPE_PULSE_LOW


class DigitalTriggerLinkedChannelState(Enum):
    LOW = saleae_pb2.DIGITAL_TRIGGER_LINKED_CHANNEL_STATE_LOW
    HIGH = saleae_pb2.DIGITAL_TRIGGER_LINKED_CHANNEL_STATE_HIGH


@dataclass
class DigitalTriggerLinkedChannel:
    """Represents a digital channel that must be either high or low while the trigger event (edge or pulse) is active"""

    #: The digital channel index of the required channel
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
    #: Note, this retains the latest X seconds. If specified, the final recording length will be approximately trim_data_seconds, retaining the latest data.
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
    buffer_size_megabytes: Optional[int] = None

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


_DEFAULT_GRPC_ADDRESS = '127.0.0.1'
_DEFAULT_GRPC_PORT = 10430


class Manager:
    """
    Manager is the main class for interacting with the Logic 2 software.

    Creating a new instance of the Manager class will attempt to connect to a running instance of the Logic 2 software.

    Please review the getting started guide for instructions on preparing the Logic 2 software for API connections.
    """

    def __init__(self, *, port: int, address: str = _DEFAULT_GRPC_ADDRESS,
                 connect_timeout_seconds: Optional[float] = None,
                 grpc_channel_arguments: Optional[List[Tuple[str, Any]]] = None,
                 logic2_process: Optional[subprocess.Popen] = None,
                 ):
        """
        It is recommended that you use Manager.launch() or Manager.connect() instead of using __init__ directly.

        Create an instance of the Manager class, and connect to the Logic 2 software.

        This library currently assumes the Logic 2 software is running on the same machine, and will attempt to connect to 127.0.0.1.
        In the future, we'll add support for supplying an IP address, as well as functions to help launch local copies of the application.

        :param port: Port number. By default, Logic 2 uses port 10430.
        :param address: Address to connect to.
        :param connect_timeout_seconds: Number of seconds to attempt to connect to gRPC server, after which an exception will be thrown.
        :param grpc_channel_arguments: A set of arguments to pass through to gRPC.
        :param logic2_process: Process object for Logic2 if launched from Python. The process will be shutdown automatically when
                               Manager.close() is called.

        """
        self.logic2_process = logic2_process
        self.channel = grpc.insecure_channel(f"{address}:{port}", options=grpc_channel_arguments)
        self.channel.subscribe(lambda value: logger.info(f"sub {value}"))
        self._stub = saleae_pb2_grpc.ManagerStub(self.channel)

        connect_timeout_seconds = 20.0 if connect_timeout_seconds is None else connect_timeout_seconds

        def cleanup():
            # Immediately close the gRPC channel to avoid the process from hanging
            self.channel.close()

            # Close the Logic2 process if it was launched from here
            if logic2_process is not None:
                logic2_process.terminate()
                logic2_process.wait(2.0)

        # Attempt to connect to endpoint
        start_time = time.monotonic()
        while True:
            try:
                app_info = self.get_app_info()

                if logic2_process:
                    if logic2_process.pid != app_info.app_pid:
                        raise errors.Logic2AlreadyRunningError()

                if app_info.api_version.major != saleae_pb2.THIS_API_VERSION_MAJOR:
                    logger.error(
                            "Incompatible Saleae Automation API Version encountered."
                            + f"Supported Major Version={saleae_pb2.THIS_API_VERSION_MAJOR}, "
                            + f"Logic2 Version={app_info.api_version.major}.{app_info.api_version.minor}.{app_info.api_version.patch}"
                        )
                    raise errors.IncompatibleApiVersionError()

                break
            except grpc.RpcError as exc:
                now = time.monotonic()
                if (exc.code() != grpc.StatusCode.UNAVAILABLE) or (now - start_time) >= connect_timeout_seconds:
                    # Rethrow if X seconds have passed or this is not a connection error
                    cleanup()
                    raise exc from None
            except Exception as exc:
                cleanup()
                raise exc from None

    @classmethod
    def launch(cls,
               application_path: Optional[Union[Path, str]] = None,
               connect_timeout_seconds: Optional[float] = None,
               grpc_channel_arguments: Optional[List[Tuple[str, Any]]] = None,
               port: Optional[int] = None) -> 'Manager':
        """
        Launch the Logic2 application and shut it down when the returned Manager is closed.

        :param application_path: The path to the Logic2 binary to run. If not specified,
                                 a locally installed copy of Logic2 will be searched for.
        :param connect_timeout_seconds: See __init__
        :param grpc_channel_arguments: See __init__
        :param port: Port to use for the gRPC server. If not specified, 10430 will be used.

        """

        # Attempt to find application
        import platform
        import os

        system = platform.system()

        def fail(reason: str):
            raise RuntimeError(f"Logic2 application not found: {reason}")

        if application_path is None:
            if system == 'Linux':
                raise RuntimeError(f"launch_application() not supported on Linux without `application_path` specified")
            elif system == 'Windows':
                program_files_path = os.environ.get('programw6432')
                if program_files_path is None:
                    fail('"Program Files" not found')

                logic2_bin = os.path.join(program_files_path, 'Logic', 'Logic.exe')

                if not os.path.exists(logic2_bin):
                    fail('Logic2 install not found. Go to https://www.saleae.com/downloads/ to download the installer.')
            elif system == 'Darwin':
                raise RuntimeError(f"launch_application() not supported on MacOS without `application_path` specified")
            else:
                raise RuntimeError(f"Unknown system: {system}")
        else:
            logic2_bin = str(application_path)
            if not os.path.exists(logic2_bin):
                fail(f'application path "{application_path}" does not exist')

        if port is None:
            port = _DEFAULT_GRPC_PORT

        process = subprocess.Popen([logic2_bin, '--automation', '--automationPort', str(port)],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)

        if system == 'Windows':
            import win32job
            import win32api
            import win32con

            # On Windows, we use a job to ensure that the child process is shutdown when this process exits
            job = win32job.CreateJobObject(None, 'Logic2Monitor')

            # Configure job to kill child process when this process exits
            limits = win32job.QueryInformationJobObject(job, win32job.JobObjectExtendedLimitInformation)
            limits['BasicLimitInformation']['LimitFlags'] = win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            win32job.SetInformationJobObject(job, win32job.JobObjectExtendedLimitInformation, limits)

            # Get handle to child process and assign job
            child_process_handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, process.pid)
            win32job.AssignProcessToJobObject(job, child_process_handle)

            # Attach the job to the process object so that it does not get garbage collected during the lifetime of the Popen object
            process.__saleae_win32_job = job

        return cls(
            address=_DEFAULT_GRPC_ADDRESS,
            port=port,
            logic2_process=process,
            connect_timeout_seconds=connect_timeout_seconds,
            grpc_channel_arguments=grpc_channel_arguments)

    @classmethod
    def connect(cls,
                *,
                address: str = _DEFAULT_GRPC_ADDRESS,
                port: int = _DEFAULT_GRPC_PORT,
                connect_timeout_seconds: Optional[float] = None,
                grpc_channel_arguments: Optional[List[Tuple[str, Any]]] = None) -> 'Manager':
        """Connect to an existing instance of Logic 2.

        :param port: Port number. By default, Logic 2 uses port 10430.
        :param address: Address to connect to.
        :param connect_timeout_seconds: See __init__
        :param grpc_channel_arguments: See __init__
        """

        return cls(address=address,
                   port=port,
                   connect_timeout_seconds=connect_timeout_seconds,
                   grpc_channel_arguments=grpc_channel_arguments)

    def get_app_info(self) -> AppInfo:
        """Get information about the connected Logic 2 instance.

        :return: AppInfo object for the connected Logic 2 instance.
        """
        with errors._error_handler():
            reply: saleae_pb2.GetAppInfoReply = self.stub.GetAppInfo(saleae_pb2.GetAppInfoRequest())

        return AppInfo(
            api_version=Version(
                major=reply.app_info.api_version.major,
                minor=reply.app_info.api_version.minor,
                patch=reply.app_info.api_version.patch,
            ),
            app_version=reply.app_info.application_version,
            app_pid=reply.app_info.launch_pid,
        )

    def close(self):
        """
        Close connection to Saleae backend, and shut it down if it was created by Manager.

        """
        self.channel.close()
        self.channel = None
        self._stub = None

        if self.logic2_process:
            import signal

            try:
                self.logic2_process.terminate()
                self.logic2_process.wait(2.0)
            except:
                pass
            self.logic2_process = None

    @property
    def stub(self) -> saleae_pb2_grpc.ManagerStub:
        """
        :meta private:
        """
        if self._stub is None:
            raise RuntimeError("Cannot use Manager after it has been closed")
        return self._stub

    def get_devices(self, *, include_simulation_devices: bool = False) -> List[DeviceDesc]:
        """
        Returns a list of connected devices. Use this to find the device id of the attached devices.

        :param include_simulation_devices: If True, the return value will also include simulation devices. This can be useful for testing without a physical device.
        """
        request = saleae_pb2.GetDevicesRequest(include_simulation_devices=include_simulation_devices)
        with errors._error_handler():
            reply: saleae_pb2.GetDevicesReply = self.stub.GetDevices(request)

        devices = []
        for device in reply.devices:
            devices.append(DeviceDesc(
                device_id=device.device_id,
                device_type=DeviceType(device.device_type),
                is_simulation=device.is_simulation,
            ))

        return devices

    def start_capture(
        self,
        *,
        device_configuration: DeviceConfiguration,
        device_id: Optional[str] = None,
        capture_configuration: Optional[CaptureConfiguration] = None,
    ) -> "Capture":
        """Start a new capture

        All capture settings need to be provided. The existing software settings, like selected device or added analyzers, are ignored.

        Be sure to catch DeviceError exceptions raised by this function, and handle them accordingly. See the error section of the library documentation.

        :param device_configuration: An instance of LogicDeviceConfiguration, complete with enabled channels, sample rates, and more.
        :param device_id: The id of device to record with.
        :param capture_configuration: The capture configuration, which selects the capture mode: timer, digital trigger, or manual., defaults to None, indicating manual mode.
        :return: Capture instance class. Be sure to call either wait() or stop() before trying to save, export, or close the capture.
        """
        request = saleae_pb2.StartCaptureRequest()

        if device_id is not None:
            request.device_id = device_id

        if isinstance(device_configuration, LogicDeviceConfiguration):
            request.logic_device_configuration.logic_channels.CopyFrom(
                saleae_pb2.LogicChannels(
                    digital_channels=device_configuration.enabled_digital_channels,
                    analog_channels=device_configuration.enabled_analog_channels,
                )
            )

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
            if capture_configuration.buffer_size_megabytes:
                request.capture_configuration.buffer_size_megabytes = (
                    capture_configuration.buffer_size_megabytes
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

        with errors._error_handler():
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
        with errors._error_handler():
            reply: saleae_pb2.LoadCaptureReply = self.stub.LoadCapture(request)

        return Capture(self, reply.capture_info.capture_id)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
