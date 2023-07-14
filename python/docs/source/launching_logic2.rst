.. _launching-and-starting-socket:

Launching the Logic 2 Software and Starting the Socket Interface
****************************************************************

The software can be launched with the automation server enabled with the following commands:

.. code-block:: bash
  
  # windows cmd
  Logic.exe --automation

  # Windows powershell
  .\Logic.exe --automation
  
  # MacOS
  ./Logic2/Contents/MacOS/Logic --automation
  
  # Linux
  ./Logic-2.4.0-master.AppImage --automation
  
  # By default, the gRPC server port number is 10430. However, it can be set with --automationPort N
  # Note: When using --automationPort, you will still need to pass --automation to enable the gRPC server.
  # Example:
  Logic.exe --automation --automationPort 10500
  

Note, the command line argument needs to be set in order for the automation interface to be enabled by default.

Additionally, the automation interface can be manually enabled in the UI by following the instructions in the :doc:`getting_started`.
