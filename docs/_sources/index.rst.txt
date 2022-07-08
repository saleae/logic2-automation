.. Saleae documentation master file, created by
   sphinx-quickstart on Fri Jul  8 13:27:35 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Saleae Logic 2 Automation Interface Documentation
=================================================

The Logic 2 Automation Interface allows developers to automate the Saleae Logic 2 software.

This API is pre-release, and subject to breaking changes before it is ready for release and production use. Please be aware that any projects built on top of the pre-release API will need to be updated once the first production version is released.

The API is exposed via gRPC (https://grpc.io/), and the gRPC proto is available to usage directly. This documentation covers the Saleae created python library, which wraps the gRPC interface. Other languages can still be used with the gRPC interface directly.


.. toctree::
   :maxdepth: 4
   :caption: Contents:

   getting_started
   launching_logic2
   automation
   errors

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

