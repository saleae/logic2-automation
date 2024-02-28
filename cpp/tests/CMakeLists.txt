find_package(Catch2 3 REQUIRED)
add_executable(TestSaleaeAutomation test_saleae_automation.cpp)
target_link_libraries(TestSaleaeAutomation
                      PRIVATE
                          saleae-automation
                          Catch2::Catch2WithMain)

include(CTest)
include(Catch)
catch_discover_tests(TestSaleaeAutomation)
