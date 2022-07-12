from saleae import automation
import os
import os.path
from datetime import datetime

# Connect to the running Logic 2 Application on port `10430`
manager = automation.Manager(port=10430)

# Configure the capturing device to record on digital channels 0, 1, 2, and 3,
# with a sampling rate of 10 MSa/s, and a logic level of 3.3V.
device_configuration = automation.LogicDeviceConfiguration(
    enabled_digital_channels=[0, 1, 2, 3],
    digital_sample_rate=10_000_000,
    digital_threshold_volts=3.3,
)

# Record 5 seconds of data before stopping the capture
capture_configuration = automation.CaptureConfiguration(
    capture_mode=automation.TimedCaptureMode(duration_seconds=5.0)
)

# Start a capture - the capture will be automatically closed when leaving the `with` block
with manager.start_capture(device_serial_number='F4241',
                           device_configuration=device_configuration,
                           capture_configuration=capture_configuration) as capture:

    # Wait until the capture has finished
    # This will take about 5 seconds because we are using a timed capture mode
    capture.wait()

    # Add an analyzer to the capture
    # Note: The simulator output is not actual SPI data
    spi_analyzer = capture.add_analyzer('SPI', label=f'Test Analyzer', settings={
        'MISO': 0,
        'Clock': 1,
        'Enable': 2,
        'Bits per Transfer': '8 Bits per Transfer (Standard)'
    })

    # Store output in a timestamped directory
    output_dir = os.path.join(os.getcwd(), f'output-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
    os.makedirs(output_dir)

    # Export analyzer data to a CSV file
    analyzer_export_filepath = os.path.join(output_dir, 'spi_export.csv')
    capture.export_data_table(
        filepath=analyzer_export_filepath,
        analyzers=[spi_analyzer],
        radix=automation.RadixType.ASCII
    )

    # Export raw digital data to a CSV file
    capture.export_raw_data_csv(directory=output_dir, digital_channels=[0, 1, 2, 3])

    # Finally, save the capture to a file
    capture_filepath = os.path.join(output_dir, 'example_capture.sal')
    capture.save_capture(filepath=capture_filepath)

# Close the connection
manager.close()