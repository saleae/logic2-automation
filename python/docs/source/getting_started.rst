Getting Started
***************

Installing the Python Automation API package
--------------------------------------------

To get started, you will need the latest build of the Logic 2 Software (2.3.56+), the logic2-automation python package, and python 3.9 or newer.

First, let's install the logic2-automation package. Download the package zip file, and install it like so:

Download the package: :download:`_static/logic2_automation-0.0.1-py3-none-any.whl`

And install it via pip:

.. code-block:: bash

  pip install path/to/logic2_automation-0.0.1-py3-none-any.whl


Launching Logic2
----------------

Because this feature is pre-release, the automation functionality is not available in the software by default. To activate it, the software needs to be launched with an environment variable:

.. code-block:: bash

  # cmd.exe
  set ENABLE_AUTOMATION=1
  # bash
  export ENABLE_AUTOMATION=1
  # powershell
  $Env:ENABLE_AUTOMATION=1

With this flag set, the automation interface can now be enabled in the software UI. Open the preferences dialog from the main menu, and scroll to the bottom.

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

Also, for most automated applications, you won't want to start the software manually. See :ref:`this section<launching-and-starting-socket>` for more information about different ways to launch the Logic software, including through this python library.

.. _device-serial-number:

Finding the Serial Number of a Device
-------------------------------------

To find the serial number of a connected device, open capture info sidebar and click the device dropdown in the top right:

.. image:: _static/device_info.png

If the device you want the serial number for is not selected, select it. Then click "Device Info" - this will open a popup with information about your device, including its serial number.

.. image:: _static/device_serial.png

You can copy the serial number from here and use it in your Python script.