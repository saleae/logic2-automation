#ifndef SALEAE_AUTOMATION_CAPTURE_HPP
#define SALEAE_AUTOMATION_CAPTURE_HPP

#include "saleae/automation/manager.hpp"
#include <optional>
#include <string_view>
#include <unordered_map>
#include <variant>
#include <string>

namespace saleae::automation {

struct AnalyzerHandle {
    int analyzerId;
};

class Capture {
public:
    using AnalyzerSettingType = std::variant<
        bool,
        std::string_view,
        int,
        float>;

    auto AddAnalyzer(
        std::string_view name,
        std::optional<std::string_view> label = std::nullopt,
        std::unordered_map<std::string_view, AnalyzerSettingType> settings = {}
    ) -> AnalyzerHandle;

    Capture(AutomationManager* manager, unsigned long captureId);

    /// @brief Stops the capture.
    void Stop();

    // TODO(mvejnovic): These need to be private.
    Capture();
    ~Capture();

    auto GetId() -> unsigned long;
    auto IsRunning() -> bool;

    /// @brief Saves the capture to a .sal file.
    void SaveCapture(std::string path);

private:
    struct Impl;
    std::unique_ptr<Impl> pImpl_;
};

}; // namespace saleae::automation

#endif // SALEAE_AUTOMATION_CAPTURE_HPP
