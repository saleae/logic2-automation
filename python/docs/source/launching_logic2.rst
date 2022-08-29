.. _launching-and-starting-socket:

Launching the Logic 2 Software and Starting the Socket Interface
****************************************************************

We'll be adding functionality to the python library to launch the Logic 2 software soon, but it's not available yet.

In the meantime, the software can be launched with the automation server enabled with the following commands:

.. code-block:: bash
  
  # windows cmd
  set ENABLE_AUTOMATION=1
  Logic.exe --automation
  
  # MacOS
  export ENABLE_AUTOMATION=1
  ./Logic2/Contents/MacOS/Logic --automation
  
  # Linux
  export ENABLE_AUTOMATION=1
  ./Logic-2.3.59-master.AppImage --automation
  
  # Windows powershell
  $Env:ENABLE_AUTOMATION=1
  .\Logic.exe --automation
  
  # by default, the port number is 10430. However, it can be set with --automationPort N

Note, both the environment variable and the command line argument need to be set in order for the automation interface to be enabled by default.

Additionally, the automation interface can be manually enabled in the UI by following the instructions in the :doc:`getting_started`.
