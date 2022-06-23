cmake_minimum_required(VERSION 3.14)

set(CMAKE_TOOLCHAIN_FILE "${CMAKE_CURRENT_SOURCE_DIR}/vcpkg/scripts/buildsystems/vcpkg.cmake"
  CACHE STRING "Vcpkg toolchain file")

project(automation_client)

find_package(gRPC CONFIG REQUIRED)
find_package(protobuf CONFIG REQUIRED)

if(WIN32)
  set(GRPC_CPP_EXE "grpc_cpp_plugin.exe")
else()
  set(GRPC_CPP_EXE "grpc_cpp_plugin")
endif()

find_path(GRPC_CPP_PLUGIN_PATH NAME ${GRPC_CPP_EXE} PATHS ${CMAKE_PROGRAM_PATH})
add_custom_command(
  OUTPUT
  grpc_gen/saleae/grpc/saleae.grpc.pb.cc
  grpc_gen/saleae/grpc/saleae.grpc.pb.h
  grpc_gen/saleae/grpc/saleae.pb.cc
  grpc_gen/saleae/grpc/saleae.pb.h
  COMMAND
  ${PROTOBUF_PROTOC_EXECUTABLE} --plugin=protoc-gen-grpc_cpp=${GRPC_CPP_PLUGIN_PATH}/${GRPC_CPP_EXE} --cpp_out=${CMAKE_CURRENT_BINARY_DIR}/grpc_gen --grpc_cpp_out=${CMAKE_CURRENT_BINARY_DIR}/grpc_gen -I ${CMAKE_CURRENT_SOURCE_DIR}/../proto ${CMAKE_CURRENT_SOURCE_DIR}/../proto/saleae/grpc/saleae.proto
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/../proto/saleae/grpc/saleae.proto
)

project(automation_cpp_client)

set(sources
  src/main.cpp
  ${CMAKE_CURRENT_BINARY_DIR}/grpc_gen/saleae/grpc/saleae.grpc.pb.cc
  ${CMAKE_CURRENT_BINARY_DIR}/grpc_gen/saleae/grpc/saleae.pb.cc
)

add_executable(${PROJECT_NAME} ${sources})

target_link_libraries(${PROJECT_NAME} PRIVATE
  gRPC::grpc++_reflection
  protobuf::libprotobuf
)

target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/grpc_gen)
