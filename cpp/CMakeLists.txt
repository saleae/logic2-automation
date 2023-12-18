cmake_minimum_required(VERSION 3.1)

project(saleae-automation
        VERSION 0.1.0
        LANGUAGES CXX)

find_program(grpc_cpp_plugin grpc_cpp_plugin)

set(PROTOBUF_PROTOC protoc)
set(PROTO_PATH "${CMAKE_SOURCE_DIR}/../proto")
set(SALEAE_GRPC_PROTO_PATH "${PROTO_PATH}/saleae/grpc/saleae.proto")

set(CMAKE_CXX_STANDARD 17)

add_custom_command(
    OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/saleae/grpc/saleae.grpc.pb.h"
           "${CMAKE_CURRENT_BINARY_DIR}/saleae/grpc/saleae.grpc.pb.cc"
    COMMAND ${PROTOBUF_PROTOC}
    ARGS --grpc_out "${CMAKE_CURRENT_BINARY_DIR}"
        --cpp_out "${CMAKE_CURRENT_BINARY_DIR}"
        -I "${PROTO_PATH}"
        --plugin=protoc-gen-grpc=${grpc_cpp_plugin}
        "${SALEAE_GRPC_PROTO_PATH}"
    DEPENDS "${SALEAE_GRPC_PROTO_PATH}"
)

add_library(saleae-automation
            src/saleae/automation/manager.cpp
            "${CMAKE_CURRENT_BINARY_DIR}/saleae/grpc/saleae.grpc.pb.cc"
            "${CMAKE_CURRENT_BINARY_DIR}/saleae/grpc/saleae.pb.cc")
target_compile_features(saleae-automation PRIVATE cxx_std_17)
target_link_libraries(saleae-automation
                      grpc++ absl_synchronization protobuf)

target_include_directories(saleae-automation
                           PUBLIC include
                           PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")

add_subdirectory(tests)
