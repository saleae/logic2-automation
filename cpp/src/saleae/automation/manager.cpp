#include "saleae/automation/manager.hpp"
#include "saleae/automation/errors.hpp"
#include "saleae/automation/models.hpp"
#include "saleae/grpc/saleae.grpc.pb.h"
#include <functional>
#include <grpcpp/client_context.h>
#include <grpcpp/support/status.h>
#include <memory>
#include <grpcpp/grpcpp.h>
#include <string_view>
#include <unordered_map>
#include "saleae/automation/private/grpc_adapters.hpp"
#include "saleae/grpc/saleae.pb.h"
#include <regex>
#include <optional>

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
        return Deserialize(reply);
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
    return pImpl_->Query<GetAppInfoReply>(
        [](auto context, auto stub, auto pReply) {
            return stub->GetAppInfo(context, {}, pReply);
        }
    );
}

auto AutomationManager::GetDevices() -> std::vector<DeviceDescriptor> const {
    return pImpl_->Query<GetDevicesReply>(
        [](auto context, auto stub, auto pReply) {
            return stub->GetDevices(context, {}, pReply);
        }
    );
}

} // namespace saleae::automation
