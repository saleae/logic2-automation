Getting Started
***************

Installing the Python Automation API package
--------------------------------------------

To get started, you will need the latest build of the Logic 2 Software (2.4.0+), the logic2-automation (1.0.0+) python package, and Python 3.8, 3.9, or 3.10.

First, let's install the logic2-automation package:

.. code-block:: bash

  pip install logic2-automation


Launching Logic2
----------------

The automation interface can be enabled in the software UI. Open the preferences dialog from the main menu, and scroll to the bottom.

.. image:: _static/server_ui.png

When the checkbox is checked, the automation server will start running in the Logic 2 software on the default port, 10430.


Using the Python Automation API
-------------------------------

Next, let's run a simple example. You don't need to have a device connected for this.
This example uses a demo device, if you would like to use a connected device follow the
steps :ref:`here<device-serial-number>` 
to find your device's serial number and replace the demo value in the example.

Create a new python file called :code:`saleae_example.py`, and paste in these contents:

.. literalinclude:: _static/saleae_example.py

With the software is running, and the automation interface enabled (as shown above), run the script:

.. code-block:: bash

  python saleae_example.py

There you have it! Take a look at the documentation for Manager and Capture to see how the functionality all works!

Also, for most automated applications, you won't want to start the software manually. See :ref:`this section<launching-and-starting-socket>` for more information about different ways to launch the Logic software.

.. _device-serial-number:

Finding the Serial Number (Device Id) of a Device
-------------------------------------------------

To find the serial number of a connected device, open capture info sidebar and click the device dropdown in the top right:

.. image:: _static/device_info.png

If the device you want the serial number for is not selected, select it. Then click "Device Info" - this will open a popup with information about your device, including its serial number.

.. image:: _static/device_serial.png

You can copy the serial number from here and use it in your Python script where a "device_id" is required.


Versioning
----------

The `saleae.proto` file contains a version (`major.minor.patch`). It can be found in the file header, and also in the
`ThisApiVersion` enum.

When generating language bindings, you can get the version of the .proto that was used through the protobuf `ThisApiVersion` enum - `THIS_API_VERSION_MAJOR`, `THIS_API_VERSION_MINOR`, and `THIS_API_VERSION_PATCH`.

The version of the .proto file that the server is using can be retrieved using the `GetAppInfo` gRPC method, or the `Manager.get_app_info()` call in the Python API.

* For a given major version, the API strives to be forward and backwards compatible.
* The major version will change when:

  * There are any breaking changes

* The minor version will change when:

  * New features are added
  * Additions are made to the existing API

* The patch version will change when:

  * There are fixes to the API


When implementing a client that uses the gRPC API directly, it is recommended to always retrieve the api version via GetAppInfo to validate that the major version is the same, and that the minor version is not older than the client. The Python API does this automatically on creation of the Manager object.

Headless on Linux
-----------------

We do not currently support running Logic 2 in a headless mode, but it is possible to run Logic 2 in headless Linux environments using XVFB.

The specifics for your environment may differ, but on Ubuntu 20.04 we have had success with the following setup.

Install xvfb and other depdendencies:

.. code-block:: bash

  sudo apt install xvfb libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libgbm1


Run Logic 2:

.. code-block:: bash

  xvfb-run path/to/Logic-2.4.0.AppImage

Troubleshooting
---------------

Failure during install due to :code:`ModuleNotFoundError: No module named 'hatchling'`
======================================================================================

:code:`logic2-automation` is packaged as a source distribution and built locally on install using :code:`hatchling`. If you are building without isolation (for example, :code:`pip install --no-build-isolation logic2-automation`) and you don't have :code:`hatchling` installed, you will see this error. If you can't install with isolation, you can install :code:`hatchling` (example: :code:`pip install hatchling`) in your local environment to resolve the issue.


Failure when importing saleae.automation / saleae.grpc
======================================================

If you see an error like this when you import from :code:`saleae.automation`, it may be a protobuf/grpc version incompatibility. This can happen when you upgrade protobuf and/or grpc after installing :code:`logic2-automation`.

.. code-block:: text

  TypeError: Descriptors cannot not be created directly.
  If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
  If you cannot immediately regenerate your protos, some other possible workarounds are:
   1. Downgrade the protobuf package to 3.20.x or lower.
   2. Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower).

You can regenerate the protobuf/grpc files by reinstalling :code:`logic2-automation`:

.. code-block:: bash

  pip install --force-reinstall logic2-automation


Can't find a solution?
======================

Contact us at https://contact.saleae.com/hc/en-us/requests/new
