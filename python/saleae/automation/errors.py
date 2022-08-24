from contextlib import contextmanager
import grpc
import re

from saleae.grpc import saleae_pb2

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


class Logic2AlreadyRunningError(SaleaeError):
    """
    This indicates that there was an instance of Logic 2 already running.

    """

    pass


class IncompatibleApiVersionError(SaleaeError):
    """
    This indicates that the server is running an incompatible API version. This only happens on major
    version changes. It is recommended to upgrade to the latest release of Logic 2 and the Python API

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


class OutOfMemoryError(CaptureError):
    """
    This exception indicates that the capture was automatically terminated because the capture buffer was filled.
    """

    pass



@contextmanager
def _error_handler():
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
    saleae_pb2.ERROR_CODE_OUT_OF_MEMORY: OutOfMemoryError,
}


def grpc_error_msg_to_exception(msg: str):
    match = error_message_re.match(msg)
    if match is None:
        return UnknownError(msg)

    code = int(match.group(1))
    error_msg = match.group(2)

    exc_type = grpc_error_code_to_exception_type.get(code, UnknownError)
    return exc_type(error_msg)

