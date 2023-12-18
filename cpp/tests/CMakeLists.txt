add_executable(TestConnection test_connection.cpp)
target_link_libraries(TestConnection saleae-automation)
add_test(TestConnection COMMAND TestConnection)

add_executable(TestDevices test_devices.cpp)
target_link_libraries(TestDevices saleae-automation)
add_test(TestDevices COMMAND TestDevices)
