#include "saleae/automation/manager.hpp"

#include <iostream>

int main() {
    const auto manager = saleae::automation::AutomationManager::Connect();
    const auto appInfo = manager->GetAppInfo();

    std::cout << appInfo.appVersion << std::endl;

    return 0;
}
