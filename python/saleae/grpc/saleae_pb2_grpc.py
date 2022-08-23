# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from saleae.grpc import saleae_pb2 as saleae_dot_grpc_dot_saleae__pb2


class ManagerStub(object):
    """Saleae Logic 2 Automation API

    ****************************************************************************

    gRPC API

    **************************************************************************

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAppInfo = channel.unary_unary(
                '/saleae.automation.Manager/GetAppInfo',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.GetAppInfoRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.GetAppInfoReply.FromString,
                )
        self.GetDevices = channel.unary_unary(
                '/saleae.automation.Manager/GetDevices',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.GetDevicesRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.GetDevicesReply.FromString,
                )
        self.StartCapture = channel.unary_unary(
                '/saleae.automation.Manager/StartCapture',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.StartCaptureRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.StartCaptureReply.FromString,
                )
        self.StopCapture = channel.unary_unary(
                '/saleae.automation.Manager/StopCapture',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.StopCaptureRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.StopCaptureReply.FromString,
                )
        self.WaitCapture = channel.unary_unary(
                '/saleae.automation.Manager/WaitCapture',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.WaitCaptureRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.WaitCaptureReply.FromString,
                )
        self.LoadCapture = channel.unary_unary(
                '/saleae.automation.Manager/LoadCapture',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.LoadCaptureRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.LoadCaptureReply.FromString,
                )
        self.SaveCapture = channel.unary_unary(
                '/saleae.automation.Manager/SaveCapture',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.SaveCaptureRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.SaveCaptureReply.FromString,
                )
        self.CloseCapture = channel.unary_unary(
                '/saleae.automation.Manager/CloseCapture',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.CloseCaptureRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.CloseCaptureReply.FromString,
                )
        self.AddAnalyzer = channel.unary_unary(
                '/saleae.automation.Manager/AddAnalyzer',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.AddAnalyzerRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.AddAnalyzerReply.FromString,
                )
        self.RemoveAnalyzer = channel.unary_unary(
                '/saleae.automation.Manager/RemoveAnalyzer',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.RemoveAnalyzerRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.RemoveAnalyzerReply.FromString,
                )
        self.AddHighLevelAnalyzer = channel.unary_unary(
                '/saleae.automation.Manager/AddHighLevelAnalyzer',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.AddHighLevelAnalyzerRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.AddHighLevelAnalyzerReply.FromString,
                )
        self.ExportRawDataCsv = channel.unary_unary(
                '/saleae.automation.Manager/ExportRawDataCsv',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.ExportRawDataCsvRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.ExportRawDataCsvReply.FromString,
                )
        self.ExportRawDataBinary = channel.unary_unary(
                '/saleae.automation.Manager/ExportRawDataBinary',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.ExportRawDataBinaryRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.ExportRawDataBinaryReply.FromString,
                )
        self.ExportDataTableCsv = channel.unary_unary(
                '/saleae.automation.Manager/ExportDataTableCsv',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.ExportDataTableCsvRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.ExportDataTableCsvReply.FromString,
                )
        self.LegacyExportAnalyzer = channel.unary_unary(
                '/saleae.automation.Manager/LegacyExportAnalyzer',
                request_serializer=saleae_dot_grpc_dot_saleae__pb2.LegacyExportAnalyzerRequest.SerializeToString,
                response_deserializer=saleae_dot_grpc_dot_saleae__pb2.LegacyExportAnalyzerReply.FromString,
                )


class ManagerServicer(object):
    """Saleae Logic 2 Automation API

    ****************************************************************************

    gRPC API

    **************************************************************************

    """

    def GetAppInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDevices(self, request, context):
        """Get list of connected devices.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartCapture(self, request, context):
        """Start a capture
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StopCapture(self, request, context):
        """Stop an active capture
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WaitCapture(self, request, context):
        """Wait until a capture has completed
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LoadCapture(self, request, context):
        """Load a capture from file.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveCapture(self, request, context):
        """Save a capture to file.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CloseCapture(self, request, context):
        """Close a capture.
        Note: It is recommended to close a capture once it is no longer being used
        so that any consumed resources can be released.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddAnalyzer(self, request, context):
        """Add an analyzer to a capture.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveAnalyzer(self, request, context):
        """Remove an analyzer from a capture.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddHighLevelAnalyzer(self, request, context):
        """Add a high-level-analyzer to a capture.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExportRawDataCsv(self, request, context):
        """Export raw channel data to CSV files.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExportRawDataBinary(self, request, context):
        """Export raw channel data to binary files.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExportDataTableCsv(self, request, context):
        """Export analyzer data to CSV file.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LegacyExportAnalyzer(self, request, context):
        """Export custom analyzer export data to file.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAppInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAppInfo,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.GetAppInfoRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.GetAppInfoReply.SerializeToString,
            ),
            'GetDevices': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDevices,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.GetDevicesRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.GetDevicesReply.SerializeToString,
            ),
            'StartCapture': grpc.unary_unary_rpc_method_handler(
                    servicer.StartCapture,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.StartCaptureRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.StartCaptureReply.SerializeToString,
            ),
            'StopCapture': grpc.unary_unary_rpc_method_handler(
                    servicer.StopCapture,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.StopCaptureRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.StopCaptureReply.SerializeToString,
            ),
            'WaitCapture': grpc.unary_unary_rpc_method_handler(
                    servicer.WaitCapture,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.WaitCaptureRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.WaitCaptureReply.SerializeToString,
            ),
            'LoadCapture': grpc.unary_unary_rpc_method_handler(
                    servicer.LoadCapture,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.LoadCaptureRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.LoadCaptureReply.SerializeToString,
            ),
            'SaveCapture': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveCapture,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.SaveCaptureRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.SaveCaptureReply.SerializeToString,
            ),
            'CloseCapture': grpc.unary_unary_rpc_method_handler(
                    servicer.CloseCapture,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.CloseCaptureRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.CloseCaptureReply.SerializeToString,
            ),
            'AddAnalyzer': grpc.unary_unary_rpc_method_handler(
                    servicer.AddAnalyzer,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.AddAnalyzerRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.AddAnalyzerReply.SerializeToString,
            ),
            'RemoveAnalyzer': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveAnalyzer,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.RemoveAnalyzerRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.RemoveAnalyzerReply.SerializeToString,
            ),
            'AddHighLevelAnalyzer': grpc.unary_unary_rpc_method_handler(
                    servicer.AddHighLevelAnalyzer,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.AddHighLevelAnalyzerRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.AddHighLevelAnalyzerReply.SerializeToString,
            ),
            'ExportRawDataCsv': grpc.unary_unary_rpc_method_handler(
                    servicer.ExportRawDataCsv,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.ExportRawDataCsvRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.ExportRawDataCsvReply.SerializeToString,
            ),
            'ExportRawDataBinary': grpc.unary_unary_rpc_method_handler(
                    servicer.ExportRawDataBinary,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.ExportRawDataBinaryRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.ExportRawDataBinaryReply.SerializeToString,
            ),
            'ExportDataTableCsv': grpc.unary_unary_rpc_method_handler(
                    servicer.ExportDataTableCsv,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.ExportDataTableCsvRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.ExportDataTableCsvReply.SerializeToString,
            ),
            'LegacyExportAnalyzer': grpc.unary_unary_rpc_method_handler(
                    servicer.LegacyExportAnalyzer,
                    request_deserializer=saleae_dot_grpc_dot_saleae__pb2.LegacyExportAnalyzerRequest.FromString,
                    response_serializer=saleae_dot_grpc_dot_saleae__pb2.LegacyExportAnalyzerReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'saleae.automation.Manager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Manager(object):
    """Saleae Logic 2 Automation API

    ****************************************************************************

    gRPC API

    **************************************************************************

    """

    @staticmethod
    def GetAppInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/GetAppInfo',
            saleae_dot_grpc_dot_saleae__pb2.GetAppInfoRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.GetAppInfoReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDevices(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/GetDevices',
            saleae_dot_grpc_dot_saleae__pb2.GetDevicesRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.GetDevicesReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartCapture(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/StartCapture',
            saleae_dot_grpc_dot_saleae__pb2.StartCaptureRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.StartCaptureReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StopCapture(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/StopCapture',
            saleae_dot_grpc_dot_saleae__pb2.StopCaptureRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.StopCaptureReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def WaitCapture(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/WaitCapture',
            saleae_dot_grpc_dot_saleae__pb2.WaitCaptureRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.WaitCaptureReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LoadCapture(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/LoadCapture',
            saleae_dot_grpc_dot_saleae__pb2.LoadCaptureRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.LoadCaptureReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveCapture(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/SaveCapture',
            saleae_dot_grpc_dot_saleae__pb2.SaveCaptureRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.SaveCaptureReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CloseCapture(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/CloseCapture',
            saleae_dot_grpc_dot_saleae__pb2.CloseCaptureRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.CloseCaptureReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddAnalyzer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/AddAnalyzer',
            saleae_dot_grpc_dot_saleae__pb2.AddAnalyzerRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.AddAnalyzerReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RemoveAnalyzer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/RemoveAnalyzer',
            saleae_dot_grpc_dot_saleae__pb2.RemoveAnalyzerRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.RemoveAnalyzerReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddHighLevelAnalyzer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/AddHighLevelAnalyzer',
            saleae_dot_grpc_dot_saleae__pb2.AddHighLevelAnalyzerRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.AddHighLevelAnalyzerReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ExportRawDataCsv(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/ExportRawDataCsv',
            saleae_dot_grpc_dot_saleae__pb2.ExportRawDataCsvRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.ExportRawDataCsvReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ExportRawDataBinary(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/ExportRawDataBinary',
            saleae_dot_grpc_dot_saleae__pb2.ExportRawDataBinaryRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.ExportRawDataBinaryReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ExportDataTableCsv(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/ExportDataTableCsv',
            saleae_dot_grpc_dot_saleae__pb2.ExportDataTableCsvRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.ExportDataTableCsvReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LegacyExportAnalyzer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/saleae.automation.Manager/LegacyExportAnalyzer',
            saleae_dot_grpc_dot_saleae__pb2.LegacyExportAnalyzerRequest.SerializeToString,
            saleae_dot_grpc_dot_saleae__pb2.LegacyExportAnalyzerReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
