from os import PathLike
from typing import Optional

from saleae.grpc import saleae_pb2
from saleae.grpc import saleae_pb2_grpc

import grpc
import grpc_status.rpc_status

import logging
logger = logging.getLogger(__name__)


class Manager:
    def __init__(self, port: int):
        """
        """
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.channel.subscribe(lambda value: logger.info(f'sub {value}'))
        self.stub = saleae_pb2_grpc.ManagerStub(self.channel)

    def close(self):
        """
        Close connection to Saleae backend, and shut it down if it was created by Manager.

        """

    def load_capture(self, filepath: str) -> 'Capture':
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

    def export_raw_data_csv(self, directory: str, *, channels: Optional[list[int]] = None,
                            analog_downsample_ratio: int = 1, iso8601: bool = False):
        request = saleae_pb2.ExportRawDataCsvRequest(
            directory=directory,
            channels=channels,
            analog_downsample_ratio=analog_downsample_ratio,
            iso8601=iso8601
        )
        self.manager.stub.ExportRawDataCsv(request)

    def close(self):
        request = saleae_pb2.CloseCaptureRequest(capture_id=self.capture_id)
        self.manager.stub.CloseCapture(request)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO)

    manager = Manager(port=50051)
    with manager.load_capture('') as cap:
        cap.close()
