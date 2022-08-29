Errors
******

The Logic 2 Automation Interface will return errors in certain situations. These errors fall into two main categories:


1. Errors produced by misuse of the API. These errors will contained detailed information about exactly why the command failed, and in some cases, list out what parameter was invalid, as well as the valid options. Be sure to read each error message closely! If these errors occur in production, it may mean there are still bugs in your code. These should not be handled in code.
2. Occasional errors while recording due to USB connectivity problems. These are rare errors, but they can occur at random - like if another USB device consumes a spike of bandwidth, causing the logic analyzer stream buffer to overflow, stopping the capture. We recommend that the developer handle these errors, and restart the capture as appropriate.

You will want to catch `CaptureError`  errors raised by `start_capture`, `stop`, and `wait`. If an error occurs during the capture start process, then `start_capture` will raise an error. If an error occurs during the capture, for example if the software wasn’t able to receive data over USB fast enough, then the capture will end prematurely. However, the python client won’t be aware of this until stop or wait is called, at which point `CaptureError` will be raised.

If any of these commands raise the `CaptureError` exception, we recommend simply starting a new capture. if `stop` or `wait` raise the error, be sure to dispose of the capture before starting the next one.

.. autoclass:: saleae.automation.SaleaeError
   :members:
   :undoc-members:

.. autoclass:: saleae.automation.UnknownError
   :members:
   :undoc-members:

.. autoclass:: saleae.automation.InternalServerError
   :members:
   :undoc-members:

.. autoclass:: saleae.automation.InvalidRequestError
   :members:
   :undoc-members:

.. autoclass:: saleae.automation.LoadCaptureFailedError
   :members:
   :undoc-members:

.. autoclass:: saleae.automation.ExportError
   :members:
   :undoc-members:

.. autoclass:: saleae.automation.MissingDeviceError
   :members:
   :undoc-members:

.. autoclass:: saleae.automation.CaptureError
   :members:
   :undoc-members:

.. autoclass:: saleae.automation.DeviceError
   :members:
   :undoc-members:

.. autoclass:: saleae.automation.OutOfMemoryError
   :members:
   :undoc-members:
