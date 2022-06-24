from concurrent import futures
import logging

from saleae.grpc import saleae_pb2, saleae_pb2_grpc

import grpc


logger = logging.getLogger(__name__)


def raise_grpc_error(context, code: int, message: str):
    # This method call will internally raise an exception
    context.abort(grpc.StatusCode.INTERNAL, f"{code}: Invalid Capture ID")


class Manager(saleae_pb2_grpc.ManagerServicer):
    def __init__(self):
        self.capture_id = 100
        self.open_captures = []

    def GetDevices(self, request, context):
        print("GetDevices called")
        devices = []
        for i in range(10):
            devices.append(
                saleae_pb2.Device(device_id=i, device_type=saleae_pb2.DeviceType.values()[
                                  i % 3], serial_number=f'{i}'),
            )
        return saleae_pb2.GetDevicesReply(devices=devices)

    def LoadCapture(self, request, context):
        self.capture_id += 1
        print(f"Loading capture, id={self.capture_id}")
        self.open_captures.append(self.capture_id)
        return saleae_pb2.LoadCaptureReply(
            capture_info=saleae_pb2.CaptureInfo(capture_id=self.capture_id)
        )

    def CloseCapture(self, request, context: grpc.ServicerContext):
        print(f'Closing capture, id={request.capture_id}')
        if request.capture_id not in self.open_captures:
            raise_grpc_error(
                context, saleae_pb2.INVALID_CAPTURE_ID, "Invalid Channel ID")
        self.open_captures.remove(request.capture_id)
        return saleae_pb2.CloseCaptureReply()

    def ExportRawDataCsv(self, request, context):
        print('export raw data')
        return saleae_pb2.ExportRawDataCsvReply(
        )



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saleae_pb2_grpc.add_ManagerServicer_to_server(Manager(), server)
    server.add_insecure_port('127.0.0.1:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
