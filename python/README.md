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
