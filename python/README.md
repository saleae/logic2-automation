## Setup

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## Building .whl

Run the following commands to generate a distributable package:

```
python -m pip install --upgrade build
python -m build
```

## Changelog

### 1.0.1

- Change `grpc` & `grpc-tools` dependency to version `>=1.13.0`. This lowers the minimum version, and doesn't stick it to a specific version.

### 1.0.0

- First release
