#include "saleae/automation/manager.hpp"
#include "saleae/automation/capture.hpp"
#include "saleae/automation/models.hpp"
#include <catch2/catch_test_macros.hpp>
#include <cstdio>
#include <string>
#include <chrono>
#include <string_view>
#include <thread>
#include <fstream>

std::ifstream::pos_type GetFileSize(std::string_view filename)
{
    std::ifstream in(std::string(filename),
                     std::ifstream::ate | std::ifstream::binary);
    return in.tellg(); 
}

auto GetBaseDeviceConfig() -> saleae::automation::device::logic::Config {
    using namespace saleae::automation::device::logic;

    return {
        .analogChannels = Config::AnalogChannelCollection {
            .sampleRate = 1'250'000UL,
            .enabledChannels = {0, 1},
        },
        .digitalChannels = Config::DigitalChannelCollection {
            .sampleRate = 10'000'000UL,
            .enabledChannels = {0, 1},
        },
    };
}

auto GetDemoDevice() -> const char* { return "F4243"; }

SCENARIO("a connection can be established") {
    using namespace saleae::automation;

    GIVEN("a saleae manager connection") {
        const auto manager = AutomationManager::Connect();
        WHEN("the app info is queried") {
            const auto appInfo = manager->GetAppInfo();
            THEN("the app version major number is >= 2") {
                const auto appVersionMajor = std::stoi(
                    std::string(
                        appInfo.appVersion.substr(
                            0,
                            appInfo.appVersion.find(".")
                        )
                    )
                );
                REQUIRE(appVersionMajor >= 2);
            }

            THEN("the app pid is not zero") {
                REQUIRE(appInfo.appPid != 0);
            }
        }
    }
}

SCENARIO("a manual capture can be started and stopped") {
    using namespace saleae::automation;

    GIVEN("a saleae manager connection") {
        const auto manager = AutomationManager::Connect();

        WHEN("the capture is started") {
            using namespace device::logic;

            const auto capture = manager->StartCapture(
                GetBaseDeviceConfig(),
                { GetDemoDevice() },
                capture::Config {
                    .captureMode = capture::ManualMode {}
                }
            );

            THEN("the capture is running and is non-zero") {
                REQUIRE(capture->IsRunning());
                REQUIRE(capture->GetId() != 0);
            }

            std::this_thread::sleep_for(std::chrono::milliseconds(20));
            capture->Stop();
        }
    }
}

SCENARIO("a capture can be saved to a file") {
    using namespace saleae::automation;

    GIVEN("a 20ms saleae recording") {
        const auto manager = AutomationManager::Connect();
        const auto capture = manager->StartCapture(
            GetBaseDeviceConfig(), { GetDemoDevice() },
            capture::Config {
                .captureMode = capture::ManualMode {},
            }
        );
        std::this_thread::sleep_for(std::chrono::milliseconds(20));
        capture->Stop();

        WHEN("the capture is saved") {
            const std::string captureFile =
                std::string(std::tmpnam(nullptr)) + ".sal";

            capture->SaveCapture(captureFile);

            THEN("the resulting file size is at least 50KB") {
                REQUIRE(GetFileSize(captureFile) > 1024 * 50);
            }
        }
    }
}
