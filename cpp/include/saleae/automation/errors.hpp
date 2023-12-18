#ifndef SALEAE_AUTOMATION_ERRORS_HPP
#define SALEAE_AUTOMATION_ERRORS_HPP

#include <stdexcept>
#include <string_view>

namespace saleae::automation::errors {

struct SaleaeError : std::runtime_error {
    SaleaeError(std::string_view message) : std::runtime_error(std::string(message)) {}
private:
    SaleaeError();
};

struct UnknownError final : SaleaeError {
    UnknownError(std::string_view message) : SaleaeError(message) {}
private:
    UnknownError();
};

struct Logic2AlreadyRunningError final : SaleaeError {
    Logic2AlreadyRunningError(std::string_view message) : SaleaeError(message) {}
private:
    Logic2AlreadyRunningError();
};

struct IncompatibleApiVersionError final : SaleaeError {
    IncompatibleApiVersionError(std::string_view message) : SaleaeError(message) {}
private:
    IncompatibleApiVersionError();
};

struct InternalServerError final : SaleaeError {
    InternalServerError(std::string_view message) : SaleaeError(message) {}
private:
    InternalServerError();
};

struct InvalidRequestError final : SaleaeError {
    InvalidRequestError(std::string_view message) : SaleaeError(message) {}
private:
    InvalidRequestError();
};

struct LoadCaptureFailedError final : SaleaeError {
    LoadCaptureFailedError(std::string_view message) : SaleaeError(message) {}
private:
    LoadCaptureFailedError();
};

struct ExportError final : SaleaeError {
    ExportError(std::string_view message) : SaleaeError(message) {}
private:
    ExportError();
};

struct MissingDeviceError final : SaleaeError {
    MissingDeviceError(std::string_view message) : SaleaeError(message) {}
private:
    MissingDeviceError();
};

struct CaptureError : SaleaeError {
    CaptureError(std::string_view message) : SaleaeError(message) {}
private:
    CaptureError();
};

struct DeviceError final : CaptureError {
    DeviceError(std::string_view message) : CaptureError(message) {}
private:
    DeviceError();
};

struct OutOfMemoryError final : CaptureError {
    OutOfMemoryError(std::string_view message) : CaptureError(message) {}
private:
    OutOfMemoryError();
};

} // namespace saleae::automation::errors

#endif // SALEAE_AUTOMATION_ERRORS_HPP
