# Saleae Logic 2 Automation

`logic2-automation` implements a Python client for the [Logic 2 Automation API](https://www.saleae.com/automation/).

Documentation can be found at https://saleae.github.io/logic2-automation/


## Changelog

### 1.0.6

- Moved `grpcio-tools` to build dependencies.

### 1.0.5

- The .whl build has been fixed, and now includes the generate protobuf/grpc files.

### 1.0.4

- YANKED!
  - The protobuf files (`saleae/grpc`) generated during the .whl build were not being included in the .whl file. This was caused by the `saleae/grpc` directory being added to the .gitignore file. These ignored files have been moved to the parent directory's .gitignore, and an empty .gitignore has been added to the python directory.
- Fix boolean analyzer settings not being sent as the correct type.

### 1.0.3

- Updated the README to link out to the docs, and move build instructions to BUILD.md.
- Updated the install docs.

### 1.0.2

- Update the distribution to only include a source distribution so that gRPC/protobuf files can be generated at install time, and be based on the installed version of grpcio/grpcio-tools/protobuf.

### 1.0.1

- YANKED!
  - This release was pulled shortly after it was released due to a conflict between the latest gRPC and the generated protobuf files.
- Change `grpc` & `grpc-tools` dependency to version `>=1.13.0`. This lowers the minimum version, and doesn't stick it to a specific version.

### 1.0.0

- First release
