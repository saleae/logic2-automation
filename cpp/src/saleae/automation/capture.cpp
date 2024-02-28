#include "saleae/automation/capture.hpp"

namespace saleae::automation {

class AutomationManager;

struct Capture::Impl {
    AutomationManager* manager;
    unsigned long captureId;
    bool isRunning;
};

Capture::Capture() =default;
Capture::~Capture() =default;

Capture::Capture(AutomationManager* manager, unsigned long captureId) {
    pImpl_ = std::make_unique<Capture::Impl>();
    pImpl_->manager = manager;
    pImpl_->captureId = captureId;
    pImpl_->isRunning = true;
}

void Capture::Stop() {
    pImpl_->manager->StopCapture(pImpl_->captureId);
    pImpl_->isRunning = false;
}

auto Capture::IsRunning() -> bool {
    return pImpl_->isRunning;
}

auto Capture::GetId() -> unsigned long {
    return pImpl_->captureId;
}

void Capture::SaveCapture(std::string path) {
    return pImpl_->manager->SaveCapture(GetId(), path);
}

} // namespace saleae::automation
