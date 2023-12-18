#ifndef SALEAE_AUTOMATION_CAPTURE_HPP
#define SALEAE_AUTOMATION_CAPTURE_HPP

#include "saleae/automation/manager.hpp"
#include <optional>
#include <string_view>
#include <unordered_map>
#include <variant>

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
private:
    Capture(const AutomationManager* manager);
    friend auto AutomationManager::StartCapture() -> const Capture*;

};

}; // namespace saleae::automation

#endif // SALEAE_AUTOMATION_CAPTURE_HPP
