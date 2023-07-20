# Logic2 Automation API

Starting with 2.3.56, Logic 2 supports a gRPC API for remote automation.

Please note that the current relase is in **beta** and will likely to have breaking changes before it is officially released.

This repository contains the gRPC .proto definition file for the API, and a Python library for using the API.  You can generate gRPC bindings for other languages using the .proto file.

You can read more about the Python API at https://saleae.github.io/logic2-automation/

## Contents

 - `python/` contains the Python library around the gRPC API. We recommend reading the docs (linked above) if you would like to use the Python library.
 - `go/` contains the Go library around the gRPC API.
 - `proto/` contains the gRPC .proto definition file.

