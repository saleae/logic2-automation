from dataclasses import dataclass, field
from enum import Enum
from os import PathLike
from typing import List, Optional

from saleae.grpc import saleae_pb2
from saleae.grpc import saleae_pb2_grpc
import time

import grpc
import grpc_status.rpc_status

import os
import os.path

import logging

from saleae.grpc.saleae_pb2 import ChannelIdentifier

logger = logging.getLogger(__name__)


class DeviceConfiguration:
    pass


@dataclass
class LogicDeviceConfiguration(DeviceConfiguration):
    enabled_analog_channels: List[int] = field(default_factory=list)
    enabled_digital_channels: List[int] = field(default_factory=list)

    analog_sample_rate: Optional[int] = None
    digital_sample_rate: Optional[int] = None

    digital_threshold: Optional[float] = None


class CaptureMode(Enum):
    CIRCULAR = saleae_pb2.CaptureMode.CIRCULAR
    STOP_AFTER_TIME = saleae_pb2.CaptureMode.STOP_AFTER_TIME
    STOP_ON_DIGITAL_TRIGGER = saleae_pb2.CaptureMode.STOP_ON_DIGITAL_TRIGGER


@dataclass
class CaptureSettings:
    buffer_size: Optional[int] = None
    """Capture buffer size (in megabytes)"""

    capture_mode: Optional[CaptureMode] = None


class Manager:
    def __init__(self, port: int):
        """ """
        self.channel = grpc.insecure_channel(f"127.0.0.1:{port}")
        self.channel.subscribe(lambda value: logger.info(f"sub {value}"))
        self.stub = saleae_pb2_grpc.ManagerStub(self.channel)

    def close(self):
        """
        Close connection to Saleae backend, and shut it down if it was created by Manager.

        """

    def get_devices(self):
        request = saleae_pb2.GetDevicesRequest()
        reply: saleae_pb2.GetDevicesReply = self.stub.GetDevices(request)
        print(reply)

    def start_capture(
        self,
        *,
        device_configuration: DeviceConfiguration,
        device_serial_number: str,
        capture_settings: CaptureSettings = CaptureSettings(),
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
        else:
            raise TypeError("Invalid device configuration type")

        if capture_settings.buffer_size is not None:
            request.capture_settings.buffer_size = request.capture_settings.buffer_size
        if capture_settings.capture_mode is not None:
            request.capture_settings.capture_mode = capture_settings.capture_mode.value

        reply: saleae_pb2.StartCaptureReply = self.stub.StartCapture(request)
        return Capture(self, reply.capture_info.capture_id)

    def load_capture(self, filepath: str) -> "Capture":
        """
        Load a capture.

        The returned Capture object will be fully loaded (`wait_until_done` not required).

        Raises:
            InvalidFileError

        """
        request = saleae_pb2.LoadCaptureRequest(filepath=filepath)
        reply: saleae_pb2.LoadCaptureReply = self.stub.LoadCapture(request)
        print(reply)
        cap = Capture(self, reply.capture_info.capture_id)
        print(cap)
        return cap


class Capture:
    def __init__(self, manager: Manager, capture_id: int):
        self.manager = manager
        self.capture_id = capture_id

    def export_raw_data_csv(
        self,
        directory: str,
        *,
        analog_channels: Optional[List[int]] = None,
        digital_channels: Optional[List[int]] = None,
        analog_downsample_ratio: int = 1,
        iso8601: bool = False,
    ):
        channels = []
        if analog_channels:
            channels.extend(
                [
                    saleae_pb2.ChannelIdentifier(type=saleae_pb2.ANALOG, index=ch)
                    for ch in analog_channels
                ]
            )
        if digital_channels:
            channels.extend(
                [
                    saleae_pb2.ChannelIdentifier(type=saleae_pb2.DIGITAL, index=ch)
                    for ch in digital_channels
                ]
            )

        print("Sending export request")
        request = saleae_pb2.ExportRawDataCsvRequest(
            capture_id=self.capture_id,
            directory=directory,
            channels=channels,
            analog_downsample_ratio=analog_downsample_ratio,
            iso8601=iso8601,
        )
        self.manager.stub.ExportRawDataCsv(request)
        print("done")

    def close(self):
        request = saleae_pb2.CloseCaptureRequest(capture_id=self.capture_id)
        self.manager.stub.CloseCapture(request)

    def stop(self):
        request = saleae_pb2.StopCaptureRequest(capture_id=self.capture_id)
        self.manager.stub.StopCapture(request)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s", level=logging.INFO
    )

    manager = Manager(port=50051)
    capture = manager.start_capture(
        device_serial_number="F4241",
        device_configuration=LogicDeviceConfiguration(
            enabled_digital_channels=[3],
            digital_sample_rate=500000000,
            digital_threshold=3.3,
        ),
        capture_settings=CaptureSettings(capture_mode=CaptureMode.STOP_AFTER_TIME),
    )
