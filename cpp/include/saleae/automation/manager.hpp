/// @brief Logic control manager.
/// @author Marko Vejnovic <markovejnovic@plocca.com>
///
/// Ensure that this file does not import the protobuf generated headers. They
/// will pollute the saleae::automation namespace if imported.
#ifndef SALEAE_AUTOMATION_MANAGER_HPP
#define SALEAE_AUTOMATION_MANAGER_HPP

#include "saleae/automation/models.hpp"
#include <memory>
#include <optional>
#include <string_view>
#include <cstdint>
#include <vector>

namespace saleae::automation {

struct Capture;

class AutomationManager final {
private:
    constexpr static std::uint16_t DEFAULT_GRPC_PORT = 10430;
    constexpr static const char* DEFAULT_GRPC_ADDRESS = "127.0.0.1";

    struct impl;
    std::unique_ptr<impl> pImpl_;
    friend class Capture;

public:
    AutomationManager();
    ~AutomationManager();

    /// @brief Connect to an existing Logic 2 instance.
    static auto Connect(
        std::string_view address = DEFAULT_GRPC_ADDRESS,
        std::uint16_t port = DEFAULT_GRPC_PORT,
        long long connectTimeoutMs = -1
    ) -> std::unique_ptr<AutomationManager>;

    /// @brief Retrieve the application version of the current running Logic
    /// process.
    auto GetAppInfo() -> LogicAppInfo const;

    /// @brief Retrieve the list of devices connected and managed by the Logic
    ///        process.
    auto GetDevices() -> std::vector<device::logic::Descriptor> const;

    /// @brief Retrieve the current running capture. If no capture is running,
    ///        create a new one.
    auto StartCapture(
        device::Config deviceConfig,
        std::optional<const char*> deviceId = std::nullopt,
        std::optional<capture::Config> captureConfiguration = std::nullopt
    ) -> std::unique_ptr<Capture>;

private:
    friend class Capture;
    void StopCapture(unsigned long captureId);
    void SaveCapture(unsigned long captureId, std::string path);
};

} // namespace saleae::automation

#endif // SALEAE_AUTOMATION_MANAGER_HPP
