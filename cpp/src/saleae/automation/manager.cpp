#include "saleae/automation/manager.hpp"
#include "saleae/automation/errors.hpp"
#include "saleae/automation/models.hpp"
#include "saleae/automation/capture.hpp"
#include "saleae/grpc/saleae.grpc.pb.h"
#include <functional>
#include <grpcpp/client_context.h>
#include <grpcpp/support/status.h>
#include <memory>
#include <grpcpp/grpcpp.h>
#include <string_view>
#include <unordered_map>
#include "saleae/automation/private/grpc_adapters.hpp"
#include "saleae/automation/private/utils.hpp"
#include "saleae/grpc/saleae.pb.h"
#include <regex>
#include <optional>
#include <variant>

namespace saleae::automation {

struct AutomationManager::impl {
    std::unique_ptr<Manager::Stub> stub;

    template <typename ReplyType>
    auto Query(
        std::function<
            ::grpc::Status
            (::grpc::ClientContext* context, Manager::Stub*, ReplyType* pReply)
        > queryLambda
    ) {
        ::grpc::ClientContext context;
        ReplyType reply;
        const ::grpc::Status status = queryLambda(&context, stub.get(), &reply);
        DelegateError(status);
        return reply;
    }

    static auto ParseLogicAbortedError(
        const ::grpc::Status& status
    ) -> std::optional<std::pair<ErrorCode, std::string>> {
        // TODO(markovejnovic): Share this with the python implementaton.
        // Maybe codegen it?
        static const std::regex EXCEPTION_PARSING_REGEX =
            std::regex(R"(^(\d+): (.*)$)");

        std::smatch piecesMatch;
        std::string errorDetailsRaw = std::string(status.error_details());
        if (!std::regex_match(errorDetailsRaw, piecesMatch,
                              EXCEPTION_PARSING_REGEX)) {
            return std::nullopt;
        }

        if (piecesMatch.size() != 3) {
            return std::nullopt;
        }

        return {{
            ErrorCode(std::stoi(piecesMatch.str(1))),
            piecesMatch.str(2)
        }};
    }

    static auto GetExceptionForErrorCode(
        ErrorCode errorCode
    ) -> std::function<errors::SaleaeError (std::string_view)> {
        using namespace errors;

        static std::unordered_map<
            ErrorCode,
            std::function<SaleaeError (std::string_view)>
        > errorMap;

        if (!errorMap.empty()) {
            return errorMap.at(errorCode);
        }

        errorMap = {
            {
                ERROR_CODE_UNSPECIFIED,
                [](std::string_view msg) { return UnknownError(msg); }
            },
            {
                ERROR_CODE_INTERNAL_EXCEPTION,
                [](std::string_view msg) { return InternalServerError(msg); }
            },
            {
                ERROR_CODE_INVALID_REQUEST,
                [](std::string_view msg) { return InvalidRequestError(msg); }
            },
            {
                ERROR_CODE_LOAD_CAPTURE_FAILED,
                [](std::string_view msg) { return LoadCaptureFailedError(msg); }
            },
            {
                ERROR_CODE_EXPORT_FAILED,
                [](std::string_view msg) { return ExportError(msg); }
            },
            {
                ERROR_CODE_MISSING_DEVICE,
                [](std::string_view msg) { return MissingDeviceError(msg); }
            },
            {
                ERROR_CODE_DEVICE_ERROR,
                [](std::string_view msg) { return DeviceError(msg); }
            },
            {
                ERROR_CODE_OUT_OF_MEMORY,
                [](std::string_view msg) { return OutOfMemoryError(msg); }
            }
        };

        return errorMap.at(errorCode);
    }

    void DelegateError(const ::grpc::Status& status) {
        if (status.ok()) {
            return;
        }

        if (status.error_code() == ::grpc::StatusCode::ABORTED) {
            const auto errorPair = ParseLogicAbortedError(status);
            if (!errorPair.has_value()) {
                throw errors::UnknownError(status.error_message());
            }

            throw GetExceptionForErrorCode(errorPair->first)(errorPair->second);
        }

        throw errors::SaleaeError(status.error_message());
    }
};

AutomationManager::AutomationManager() =default;
AutomationManager::~AutomationManager() =default;

auto AutomationManager::Connect(
    std::string_view address,
    std::uint16_t port,
    long long connectTimeoutMs
) -> std::unique_ptr<AutomationManager> {
    auto manager = std::make_unique<AutomationManager>();

    const std::string channelTargetStr =
        std::string(address) + ":" + std::to_string(port);

    const auto channel = ::grpc::CreateChannel(
        channelTargetStr,
        ::grpc::InsecureChannelCredentials()
    );

    manager->pImpl_ = std::unique_ptr<AutomationManager::impl>(
        new AutomationManager::impl {
            .stub = Manager::NewStub(channel)
        }
    );

    return manager;
}

auto AutomationManager::GetAppInfo() -> LogicAppInfo const {
    return Deserialize(pImpl_->Query<GetAppInfoReply>(
        [](auto context, auto stub, auto pReply) {
            return stub->GetAppInfo(context, {}, pReply);
        }
    ));
}

auto AutomationManager::GetDevices() -> std::vector<device::logic::Descriptor> const {
    return Deserialize(pImpl_->Query<GetDevicesReply>(
        [](auto context, auto stub, auto pReply) {
            return stub->GetDevices(context, {}, pReply);
        }
    ));
}

auto AutomationManager::StartCapture(
    device::Config deviceConfig,
    std::optional<const char*> deviceId,
    std::optional<capture::Config> captureConfiguration
) -> std::unique_ptr<Capture> {
    StartCaptureRequest request;

    if (deviceId.has_value()) {
        request.set_device_id(*deviceId);
    }

    if (captureConfiguration.has_value()) {
        auto* pbufCapConf = Serialize(*captureConfiguration);
        std::cout << pbufCapConf->SerializeAsString() << std::endl;
        request.set_allocated_capture_configuration(pbufCapConf);
    }

    std::visit(overloaded{
        [&request](const device::logic::Config& config) mutable {
            request.set_allocated_logic_device_configuration(Serialize(config));
        },
        [](const auto& config) {
            throw std::runtime_error("Invalid device configuration type.");
        }
    }, deviceConfig);

    const auto captureId = pImpl_->Query<StartCaptureReply>(
        [&](auto context, auto stub, auto pReply) {
            return stub->StartCapture(context, request, pReply);
        }
    ).capture_info().capture_id();

    return std::make_unique<Capture>(this, captureId);
}

void AutomationManager::StopCapture(unsigned long captureId) {
    StopCaptureRequest request;
    request.set_capture_id(captureId);

    pImpl_->Query<StopCaptureReply>(
        [request](auto context, auto stub, auto pReply) {
            return stub->StopCapture(context, request, pReply);
        }
    );
}

void AutomationManager::SaveCapture(
    unsigned long captureId,
    std::string path
) {
    SaveCaptureRequest request;
    request.set_capture_id(captureId);
    request.set_filepath(path);

    pImpl_->Query<SaveCaptureReply>(
        [request](auto context, auto stub, auto pReply) {
            return stub->SaveCapture(context, request, pReply);
        }
    );
}

} // namespace saleae::automation
