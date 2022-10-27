from enum import Enum
from .errors import _error_handler

import saleae.automation
from saleae.grpc import saleae_pb2, saleae_pb2_grpc

from typing import List, Optional, Union, Dict
from dataclasses import dataclass


class RadixType(Enum):
    BINARY = saleae_pb2.RADIX_TYPE_BINARY
    DECIMAL = saleae_pb2.RADIX_TYPE_DECIMAL
    HEXADECIMAL = saleae_pb2.RADIX_TYPE_HEXADECIMAL
    ASCII = saleae_pb2.RADIX_TYPE_ASCII


@dataclass
class AnalyzerHandle:
    #: Internal Analyzer Id
    analyzer_id: int


@dataclass
class DataTableExportConfiguration:
    #: Analyzer to export
    analyzer: AnalyzerHandle

    #: Radix type to use for format
    radix: RadixType


@dataclass
class DataTableFilter:
    #: Columns to search
    columns: List[str]

    #: Query string
    query: str


class Capture:
    """
    This class represents a single capture in the Logic 2 software.

    This class is returned from start_capture() and from load_capture()

    In the case of start_capture(), the capture is still in the recording state, and wait() or stop() must be called before any other function can be called.

    Be sure to close() when you're finished! Otherwise, they will remain in the application as tabs, and will continue to consume memory in the background.
    """

    def __init__(self, manager: 'saleae.automation.Manager', capture_id: int):
        """
        This class cannot be constructed by the user, and is only returned from the Manager class.
        """
        self.manager = manager
        self.capture_id = capture_id

    def add_analyzer(
        self,
        name: str,
        *,
        label: Optional[str] = None,
        settings: Optional[Dict[str, Union[str, int, float, bool]]] = None,
    ) -> AnalyzerHandle:
        """Add an analyzer to the capture

        Note: analyzers already added to a loaded_capture cannot be accessed from the API at this time.

        :param name: The name of the Analyzer, as shown in the Logic 2 application add analyzer list. This must match exactly.
        :param label: The user editable display string for the analyzer. This will be shown in the analyzer data table export, defaults to None
        :param settings: All settings for the analyzer. The keys and values here must exactly match the Analyzer settings as shown in the UI, defaults to None
        :return: Returns an AnalyzerHandle
        """
        analyzer_settings = {}

        if settings is not None:
            for key, value in settings.items():
                if isinstance(value, bool):
                    v = saleae_pb2.AnalyzerSettingValue(bool_value=value)
                elif isinstance(value, str):
                    v = saleae_pb2.AnalyzerSettingValue(string_value=value)
                elif isinstance(value, int):
                    v = saleae_pb2.AnalyzerSettingValue(int64_value=value)
                elif isinstance(value, float):
                    v = saleae_pb2.AnalyzerSettingValue(double_value=value)
                else:
                    raise RuntimeError(
                        "Unsupported analyzer setting value type")

                analyzer_settings[key] = v

        request = saleae_pb2.AddAnalyzerRequest(
            capture_id=self.capture_id,
            analyzer_name=name,
            analyzer_label=label,
            settings=analyzer_settings,
        )

        with _error_handler():
            reply = self.manager.stub.AddAnalyzer(request)

        return AnalyzerHandle(analyzer_id=reply.analyzer_id)

    def add_high_level_analyzer(
        self,
        extension_directory: str,
        name: str,
        *,
        input_analyzer: AnalyzerHandle,
        settings: Optional[Dict[str, Union[str, float]]] = None,
        label: Optional[str] = None,
    ) -> AnalyzerHandle:
        """Add a high level analyzer to the capture.

        Note: high level analyzers already added to a loaded_capture cannot be accessed from the API at this time.

        :param extension_directory: The directory of the extension that the HLA is in.
        :param name: The name of the HLA, as specifiied in the extension.json of the extension.
        :param input_analyzer: Handle to analyzer (added via add_analyzer) to use as input to this HLA.
        :param settings: All settings for the analyzer. The keys and values here must match the HLA settings as shown in the HLA class.
        :param label: The user editable display string for the high level analyzer. This will be shown in the analyzer data table export.
        :return: Returns an AnalyzerHandle
        """
        analyzer_settings = {}

        if settings is not None:
            for key, value in settings.items():
                if isinstance(value, str):
                    v = saleae_pb2.HighLevelAnalyzerSettingValue(string_value=value)
                elif isinstance(value, int):
                    v = saleae_pb2.HighLevelAnalyzerSettingValue(number_value=value)
                else:
                    raise RuntimeError(
                        "Unsupported high level analyzer setting value type")

                analyzer_settings[key] = v

        request = saleae_pb2.AddHighLevelAnalyzerRequest(
            capture_id=self.capture_id,
            extension_directory=extension_directory,
            hla_name=name,
            input_analyzer_id=input_analyzer.analyzer_id,
            settings=analyzer_settings,
            hla_label=label,
        )

        with _error_handler():
            reply = self.manager.stub.AddHighLevelAnalyzer(request)

        return AnalyzerHandle(analyzer_id=reply.analyzer_id)

    def remove_analyzer(self, analyzer: AnalyzerHandle):
        """
        Removes an analyzer from the capture.

        :param analyzer: AnalyzerHandle returned by add_analyzer()
        """
        request = saleae_pb2.RemoveAnalyzerRequest(
            capture_id=self.capture_id, analyzer_id=analyzer.analyzer_id
        )
        with _error_handler():
            self.manager.stub.RemoveAnalyzer(request)

    def remove_high_level_analyzer(self, high_level_analyzer: AnalyzerHandle):
        """
        Removes a high level analyzer from the capture.

        :param high_level_analyzer: AnalyzerHandle returned by add_analyzer()
        """
        request = saleae_pb2.RemoveHighLevelAnalyzerRequest(
            capture_id=self.capture_id, analyzer_id=high_level_analyzer.analyzer_id
        )
        with _error_handler():
            self.manager.stub.RemoveHighLevelAnalyzer(request)

    def save_capture(self, filepath: str):
        """
        Saves the capture to a .sal file, which can be loaded later either through the UI or with the load_capture() function.

        :param filepath: path to the .sal file. Can be absolute, or relative to the Logic 2 software current working directory.
        """
        request = saleae_pb2.SaveCaptureRequest(
            capture_id=self.capture_id, filepath=filepath
        )

        with _error_handler():
            self.manager.stub.SaveCapture(request)

    def legacy_export_analyzer(
        self, filepath: str, analyzer: AnalyzerHandle, radix: RadixType
    ):
        """
        Exports the specified analyzer using the analyzer plugin export format, and not the data table format.

        Use the export_data_table() function to export analyzer results from the data table.

        :param filepath: file name and path to export to. Should include the file name and extension, typically .csv or .txt.
        :param analyzer: AnalyzerHandle returned from add_analyzer()
        :param radix: Display Radix, from the RadixType enumeration.
        """
        request = saleae_pb2.LegacyExportAnalyzerRequest(
            capture_id=self.capture_id,
            filepath=filepath,
            analyzer_id=analyzer.analyzer_id,
            radix_type=radix.value,
        )

        with _error_handler():
            self.manager.stub.LegacyExportAnalyzer(request)

    def export_data_table(
        self,
        filepath: str,
        analyzers: List[Union[AnalyzerHandle, DataTableExportConfiguration]],
        *,
        columns: Optional[List[str]] = None,
        filter: Optional[DataTableFilter] = None,
        iso8601_timestamp: bool = False,
    ):
        """
        Exports the Analyzer Data Table

        We will be adding more options to this in the future, including the query string, specific columns, specific query columns, and more.

        :param filepath: The specified output file, including extension, .csv.
        :param analyzers: A list of AnalyzerHandles that should be included in the export, returned from add_analyzer()
        :param columns: Columns to include in export.
        :param filter: Filter to apply to the exported data.
        :param iso8601_timestamp: Use this to output wall clock timestamps, instead of capture relative timestamps. Defaults to False.
        """
        analyzer_configs = []
        for a in analyzers:
            if isinstance(a, AnalyzerHandle):
                analyzer_configs.append(saleae_pb2.DataTableAnalyzerConfiguration(analyzer_id=a.analyzer_id))
            elif isinstance(a, DataTableExportConfiguration):
                analyzer_configs.append(saleae_pb2.DataTableAnalyzerConfiguration(
                    analyzer_id=a.analyzer.analyzer_id, radix_type=a.radix.value))
            else:
                raise RuntimeError(f"Unexpected type for analyzer: {type(a)}")

        pb_filter = None if filter is None else saleae_pb2.DataTableFilter(query=filter.query, columns=filter.columns)

        request = saleae_pb2.ExportDataTableCsvRequest(
            capture_id=self.capture_id,
            filepath=filepath,
            analyzers=analyzer_configs,
            export_columns=columns,
            filter=pb_filter,
            iso8601_timestamp=iso8601_timestamp,
        )

        with _error_handler():
            self.manager.stub.ExportDataTableCsv(request)

    def export_raw_data_csv(
        self,
        directory: str,
        *,
        analog_channels: Optional[List[int]] = None,
        digital_channels: Optional[List[int]] = None,
        analog_downsample_ratio: int = 1,
        iso8601_timestamp: bool = False,
    ):
        """Exports raw data to CSV file(s)

        This produces exactly the same format as used in the Logic 2 software when using the "Export Raw Data" dialog with the "CSV" option selected.

        Note, the directory parameter is a specific folder that must already exist, and should not include a filename.

        The export system will produce an analog.csv and/or digital.csv file(s) in that directory.

        All selected analog channels will be combined into the analog.csv file, and likewise for digital channels and digital.csv

        If no channels are specified, all channels will be exported.

        :param directory: directory path (not including a filename) to where analog.csv and/or digital.csv will be saved.
        :param analog_channels: list of analog channels to export, defaults to None
        :param digital_channels: list of digital channels to export, defaults to None
        :param analog_downsample_ratio: optional analog downsample ratio, useful to help reduce export file sizes where extra analog resolution isn't needed, defaults to 1
        :param iso8601_timestamp: Use this to output wall clock timestamps, instead of capture relative timestamps. Defaults to False.
        """
        channels = saleae_pb2.LogicChannels(
            analog_channels=[] if analog_channels is None else analog_channels,
            digital_channels=[] if digital_channels is None else digital_channels,
        )

        request = saleae_pb2.ExportRawDataCsvRequest(
            capture_id=self.capture_id,
            directory=directory,
            logic_channels=channels,
            analog_downsample_ratio=analog_downsample_ratio,
            iso8601_timestamp=iso8601_timestamp,
        )

        with _error_handler():
            self.manager.stub.ExportRawDataCsv(request)

    def export_raw_data_binary(
        self,
        directory: str,
        *,
        analog_channels: Optional[List[int]] = None,
        digital_channels: Optional[List[int]] = None,
        analog_downsample_ratio: int = 1,
    ):
        """
        Exports raw data to binary files

        This produces exactly the same format as used in the Logic 2 software when using the "Export Raw Data" dialog with the "binary" option selected.

        Documentation for the format can be found here: https://support.saleae.com/faq/technical-faq/binary-export-format-logic-2

        Note, the directory parameter is a specific folder that must already exist, and should not include a filename.

        The export system will produce one .bin file for each channel exported.

        If no channels are specified, all channels will be exported.

        :param directory: directory path (not including a filename) to where .bin files will be saved
        :param analog_channels: list of analog channels to export, defaults to None
        :param digital_channels: list of digital channels to export, defaults to None
        :param analog_downsample_ratio: optional analog downsample ratio, useful to help reduce export file sizes where extra analog resolution isn't needed, defaults to 1
        """
        channels = saleae_pb2.LogicChannels(
            analog_channels=[] if analog_channels is None else analog_channels,
            digital_channels=[] if digital_channels is None else digital_channels,
        )

        request = saleae_pb2.ExportRawDataBinaryRequest(
            capture_id=self.capture_id,
            directory=directory,
            logic_channels=channels,
            analog_downsample_ratio=analog_downsample_ratio,
        )

        with _error_handler():
            self.manager.stub.ExportRawDataBinary(request)

    def close(self):
        """
        Closes the capture. Once called, do not use this instance.
        """
        request = saleae_pb2.CloseCaptureRequest(capture_id=self.capture_id)
        with _error_handler():
            self.manager.stub.CloseCapture(request)

    def stop(self):
        """
        Stops the capture. Can be used with any capture mode, but this is recommended for use with ManualCaptureMode.

        stop() and wait() should never both be used for a single capture.

        Do not call stop() more than once.

        stop() should never be called for loaded captures.

        If an error occurred during the capture (for example, a USB read timeout, or an out of memory error) that error will be raised by this function.

        Be sure to catch DeviceError exceptions raised by this function, and handle them accordingly. See the error section of the library documentation.
        """
        request = saleae_pb2.StopCaptureRequest(capture_id=self.capture_id)
        with _error_handler():
            self.manager.stub.StopCapture(request)

    def wait(self):
        """
        Waits for the capture to complete. This should only be used with TimedCaptureMode or DigitalTriggerCaptureMode.

        for TimedCaptureMode, this will wait for the capture duration to complete.

        For DigitalTriggerCaptureMode, this will wait for the digital trigger to be found and the capture to complete.

        stop() and wait() should never both be used for a single capture.

        Do not call wait() more than once.

        wait() should never be called for loaded captures.

        Be sure to catch DeviceError exceptions raised by this function, and handle them accordingly. See the error section of the library documentation.
        """
        request = saleae_pb2.WaitCaptureRequest(capture_id=self.capture_id)
        with _error_handler():
            self.manager.stub.WaitCapture(request)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
