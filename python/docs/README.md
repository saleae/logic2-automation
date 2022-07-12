# Logic 2 Automation Python Documentation Generation

The sphinx documentation tool is used to generate the documentation for the Logic 2 automation python library.

To build the documentation:

Windows:

```batch
python -m venv .venv
.venv\Scripts\activate.bat
py -m pip install -r requirements.txt
:: build html docs
docs\make.bat html
```
