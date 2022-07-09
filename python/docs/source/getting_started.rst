Getting Started
***************

To get started, you will need the latest build of the Logic 2 Software (2.3.56+), the logic2-automation python package, and python 3.9 or newer.

First, let's install the logic2-automation package. Download the package zip file, and install it like so:

.. code-block:: bash

  pip install logic2-automation.zip

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

Next, let's run a simple example. You don't need to have a device connected for this.

Create a new python file called saleae_example.py, and paste in these contents:

.. code-block:: python

  # TODO: add python example here.

Then, run the script. Make sure the software is running, and the automation interface is enabled, as shown above.

.. code-block:: bash

  python saleae_example.py

There you have it! Take a look at the documentation for Manager and Capture to see how the functionality all works!

Also, for most automated applications, you won't want to start the software manually. See this section for more information about different ways to launch the Logic software, including through this python library.