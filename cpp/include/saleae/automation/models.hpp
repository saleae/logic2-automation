#ifndef SALEAE_AUTOMATION_APPINFO_HPP
#define SALEAE_AUTOMATION_APPINFO_HPP

#include <string_view>

namespace saleae::automation {

struct SemverVersion {
    unsigned long major;
    unsigned long minor;
    unsigned long patch;
};

struct LogicAppInfo {
    SemverVersion apiVersion;
    std::string_view appVersion;
    int appPid;
};

enum class LogicDeviceType {
    Unspecified,
    Logic,
    Logic4,
    Logic8,
    Logic16,
    LogicPro8,
    LogicPro16,
    Count
};

struct DeviceDescriptor {
    std::string_view deviceId;
    LogicDeviceType deviceType;
    bool isSimulation;
};

} // namespace saleae::automation

#endif // SALEAE_AUTOMATION_APPINFO_HPP
