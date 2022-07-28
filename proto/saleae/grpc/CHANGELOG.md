# Saleae Logic 2 gRPC API Changelog

## [0.0.2]

There are breaking changes to the `ExportDataTableRequest` message. See below for details.

### Changed

- The `ExportDataTableRequest` message has been updated to support filtering, per-analyzer radix, and a choice of columns to export.
  - **NOTE** The protobuf definition has changed in a breaking way!

## [0.0.1]

Initial release
