# Build

## Setup

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## Building .tar.gz

Run the following commands to generate a distributable source package:

```
python -m pip install --upgrade build
python -m build --sdist
```

### Why not .whl?

This package uses gRPC to communicate with the Saleae Logic2 application. This depends on using protobuf (`protoc`) to generate python files from a .proto file. If the version of protobuf used to generate the python files differs from the grpcio or protobuf version installed on the client machine there may be compatibility issues.

In particular, there was a break @ protobuf 4.21.0, released on May 6, 2022: https://developers.google.com/protocol-buffers/docs/news/2022-05-06#python-updates

Instead of distributing .whl files with generated files from a specific protobuf version, we have instead decided to release a source distribution that will generate the necessary files at install time, using the installed protobuf version.

This isn't a perfect solution - if the protobuf package is updated after generating the files, it may become incompatible. This can be resolved by reinstalling logic2-automation via pip: `pip install --force-reinstall logic2-automation`. This requires a manual step, but we think this is a good compromise that still allows users on old versions to use this package.
