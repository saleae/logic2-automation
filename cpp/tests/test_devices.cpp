#include "saleae/automation/manager.hpp"

#include <iostream>

int main() {
    const auto manager = saleae::automation::AutomationManager::Connect();
    const auto devices = manager->GetDevices();
    for (const auto& dev : devices) {
        std::cout << dev.deviceId << std::endl;
    }

    return 0;
}
