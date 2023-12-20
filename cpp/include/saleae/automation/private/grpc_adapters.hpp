#ifndef SALEAE_AUTOMATION_PRIVATE_GRPC_ADAPTER_HPP
#define SALEAE_AUTOMATION_PRIVATE_GRPC_ADAPTER_HPP

#include "saleae/grpc/saleae.pb.h"

#include "saleae/automation/models.hpp"
#include <algorithm>

namespace saleae::automation {

inline auto Deserialize(const GetAppInfoReply& reply) -> LogicAppInfo {
    const auto& appInfo = reply.app_info();

    return {
        .apiVersion = {
            .major = appInfo.api_version().major(),
            .minor = appInfo.api_version().minor(),
            .patch = appInfo.api_version().patch(),
        },
        .appVersion = appInfo.application_version(),
        .appPid = static_cast<int>(appInfo.launch_pid()),
    };
}

inline auto Deserialize(
    const GetDevicesReply& reply
) -> std::vector<device::logic::Descriptor> {
    const auto& devices = reply.devices();

    std::vector<device::logic::Descriptor> output;
    output.reserve(devices.size());

    std::transform(
        devices.cbegin(),
        devices.cend(),
        output.begin(),
        [](const Device& dev) {
            return device::logic::Descriptor {
                .deviceId = dev.device_id(),
                .deviceType = static_cast<device::logic::Type>(dev.device_type()),
                .isSimulation = dev.is_simulation(),
            };
        }
    );

    return output;
}

} // namespace saleae::automation

#endif // SALEAE_AUTOMATION_PRIVATE_GRPC_ADAPTER_HPP
