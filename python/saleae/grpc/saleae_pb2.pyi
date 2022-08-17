from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CHANNEL_TYPE_ANALOG: ChannelType
CHANNEL_TYPE_DIGITAL: ChannelType
CHANNEL_TYPE_UNSPECIFIED: ChannelType
DESCRIPTOR: _descriptor.FileDescriptor
DEVICE_TYPE_LOGIC: DeviceType
DEVICE_TYPE_LOGIC_16: DeviceType
DEVICE_TYPE_LOGIC_4: DeviceType
DEVICE_TYPE_LOGIC_8: DeviceType
DEVICE_TYPE_LOGIC_PRO_16: DeviceType
DEVICE_TYPE_LOGIC_PRO_8: DeviceType
DEVICE_TYPE_UNSPECIFIED: DeviceType
DIGITAL_TRIGGER_LINKED_CHANNEL_STATE_HIGH: DigitalTriggerLinkedChannelState
DIGITAL_TRIGGER_LINKED_CHANNEL_STATE_LOW: DigitalTriggerLinkedChannelState
DIGITAL_TRIGGER_LINKED_CHANNEL_STATE_UNSPECIFIED: DigitalTriggerLinkedChannelState
DIGITAL_TRIGGER_TYPE_FALLING: DigitalTriggerType
DIGITAL_TRIGGER_TYPE_PULSE_HIGH: DigitalTriggerType
DIGITAL_TRIGGER_TYPE_PULSE_LOW: DigitalTriggerType
DIGITAL_TRIGGER_TYPE_RISING: DigitalTriggerType
DIGITAL_TRIGGER_TYPE_UNSPECIFIED: DigitalTriggerType
ERROR_CODE_DEVICE_ERROR: ErrorCode
ERROR_CODE_EXPORT_FAILED: ErrorCode
ERROR_CODE_INTERNAL_EXCEPTION: ErrorCode
ERROR_CODE_INVALID_REQUEST: ErrorCode
ERROR_CODE_LOAD_CAPTURE_FAILED: ErrorCode
ERROR_CODE_MISSING_DEVICE: ErrorCode
ERROR_CODE_OUT_OF_MEMORY: ErrorCode
ERROR_CODE_UNSPECIFIED: ErrorCode
RADIX_TYPE_ASCII: RadixType
RADIX_TYPE_BINARY: RadixType
RADIX_TYPE_DECIMAL: RadixType
RADIX_TYPE_HEXADECIMAL: RadixType
RADIX_TYPE_UNSPECIFIED: RadixType
THIS_API_VERSION_MAJOR: ThisApiVersion
THIS_API_VERSION_MINOR: ThisApiVersion
THIS_API_VERSION_PATCH: ThisApiVersion
THIS_API_VERSION_ZERO: ThisApiVersion

class AddAnalyzerReply(_message.Message):
    __slots__ = ["analyzer_id"]
    ANALYZER_ID_FIELD_NUMBER: _ClassVar[int]
    analyzer_id: int
    def __init__(self, analyzer_id: _Optional[int] = ...) -> None: ...

class AddAnalyzerRequest(_message.Message):
    __slots__ = ["analyzer_label", "analyzer_name", "capture_id", "settings"]
    class SettingsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AnalyzerSettingValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[AnalyzerSettingValue, _Mapping]] = ...) -> None: ...
    ANALYZER_LABEL_FIELD_NUMBER: _ClassVar[int]
    ANALYZER_NAME_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    analyzer_label: str
    analyzer_name: str
    capture_id: int
    settings: _containers.MessageMap[str, AnalyzerSettingValue]
    def __init__(self, capture_id: _Optional[int] = ..., analyzer_name: _Optional[str] = ..., analyzer_label: _Optional[str] = ..., settings: _Optional[_Mapping[str, AnalyzerSettingValue]] = ...) -> None: ...

class AnalyzerSettingValue(_message.Message):
    __slots__ = ["bool_value", "double_value", "int64_value", "string_value"]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    bool_value: bool
    double_value: float
    int64_value: int
    string_value: str
    def __init__(self, string_value: _Optional[str] = ..., int64_value: _Optional[int] = ..., bool_value: bool = ..., double_value: _Optional[float] = ...) -> None: ...

class AppInfo(_message.Message):
    __slots__ = ["api_version", "application_version", "pid"]
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_VERSION_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    api_version: Version
    application_version: str
    pid: int
    def __init__(self, api_version: _Optional[_Union[Version, _Mapping]] = ..., application_version: _Optional[str] = ..., pid: _Optional[int] = ...) -> None: ...

class CaptureConfiguration(_message.Message):
    __slots__ = ["buffer_size", "digital_capture_mode", "manual_capture_mode", "timed_capture_mode"]
    BUFFER_SIZE_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_CAPTURE_MODE_FIELD_NUMBER: _ClassVar[int]
    MANUAL_CAPTURE_MODE_FIELD_NUMBER: _ClassVar[int]
    TIMED_CAPTURE_MODE_FIELD_NUMBER: _ClassVar[int]
    buffer_size: int
    digital_capture_mode: DigitalTriggerCaptureMode
    manual_capture_mode: ManualCaptureMode
    timed_capture_mode: TimedCaptureMode
    def __init__(self, buffer_size: _Optional[int] = ..., manual_capture_mode: _Optional[_Union[ManualCaptureMode, _Mapping]] = ..., timed_capture_mode: _Optional[_Union[TimedCaptureMode, _Mapping]] = ..., digital_capture_mode: _Optional[_Union[DigitalTriggerCaptureMode, _Mapping]] = ...) -> None: ...

class CaptureInfo(_message.Message):
    __slots__ = ["capture_id"]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    capture_id: int
    def __init__(self, capture_id: _Optional[int] = ...) -> None: ...

class ChannelIdentifier(_message.Message):
    __slots__ = ["device_id", "index", "type"]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    index: int
    type: ChannelType
    def __init__(self, device_id: _Optional[str] = ..., type: _Optional[_Union[ChannelType, str]] = ..., index: _Optional[int] = ...) -> None: ...

class CloseCaptureReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CloseCaptureRequest(_message.Message):
    __slots__ = ["capture_id"]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    capture_id: int
    def __init__(self, capture_id: _Optional[int] = ...) -> None: ...

class DataTableAnalyzerConfiguration(_message.Message):
    __slots__ = ["analyzer_id", "radix_type"]
    ANALYZER_ID_FIELD_NUMBER: _ClassVar[int]
    RADIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    analyzer_id: int
    radix_type: RadixType
    def __init__(self, analyzer_id: _Optional[int] = ..., radix_type: _Optional[_Union[RadixType, str]] = ...) -> None: ...

class DataTableFilter(_message.Message):
    __slots__ = ["columns", "query"]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedScalarFieldContainer[str]
    query: str
    def __init__(self, query: _Optional[str] = ..., columns: _Optional[_Iterable[str]] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ["device_id", "device_type", "is_simulation"]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_SIMULATION_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    device_type: DeviceType
    is_simulation: bool
    def __init__(self, device_id: _Optional[str] = ..., device_type: _Optional[_Union[DeviceType, str]] = ..., is_simulation: bool = ...) -> None: ...

class DigitalTriggerCaptureMode(_message.Message):
    __slots__ = ["after_trigger_seconds", "linked_channels", "max_pulse_width_seconds", "min_pulse_width_seconds", "trigger_channel_index", "trigger_type", "trim_data_seconds"]
    AFTER_TRIGGER_SECONDS_FIELD_NUMBER: _ClassVar[int]
    LINKED_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    MAX_PULSE_WIDTH_SECONDS_FIELD_NUMBER: _ClassVar[int]
    MIN_PULSE_WIDTH_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_CHANNEL_INDEX_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRIM_DATA_SECONDS_FIELD_NUMBER: _ClassVar[int]
    after_trigger_seconds: float
    linked_channels: _containers.RepeatedCompositeFieldContainer[DigitalTriggerLinkedChannel]
    max_pulse_width_seconds: float
    min_pulse_width_seconds: float
    trigger_channel_index: int
    trigger_type: DigitalTriggerType
    trim_data_seconds: float
    def __init__(self, trigger_type: _Optional[_Union[DigitalTriggerType, str]] = ..., after_trigger_seconds: _Optional[float] = ..., trim_data_seconds: _Optional[float] = ..., trigger_channel_index: _Optional[int] = ..., min_pulse_width_seconds: _Optional[float] = ..., max_pulse_width_seconds: _Optional[float] = ..., linked_channels: _Optional[_Iterable[_Union[DigitalTriggerLinkedChannel, _Mapping]]] = ...) -> None: ...

class DigitalTriggerLinkedChannel(_message.Message):
    __slots__ = ["channel_index", "state"]
    CHANNEL_INDEX_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    channel_index: int
    state: DigitalTriggerLinkedChannelState
    def __init__(self, channel_index: _Optional[int] = ..., state: _Optional[_Union[DigitalTriggerLinkedChannelState, str]] = ...) -> None: ...

class ExportAnalyzerLegacyReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ExportAnalyzerLegacyRequest(_message.Message):
    __slots__ = ["analyzer_id", "capture_id", "filepath", "radix_type"]
    ANALYZER_ID_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    FILEPATH_FIELD_NUMBER: _ClassVar[int]
    RADIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    analyzer_id: int
    capture_id: int
    filepath: str
    radix_type: RadixType
    def __init__(self, capture_id: _Optional[int] = ..., filepath: _Optional[str] = ..., analyzer_id: _Optional[int] = ..., radix_type: _Optional[_Union[RadixType, str]] = ...) -> None: ...

class ExportDataTableReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ExportDataTableRequest(_message.Message):
    __slots__ = ["analyzers", "capture_id", "export_columns", "filepath", "filter", "iso8601"]
    ANALYZERS_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    EXPORT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    FILEPATH_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ISO8601_FIELD_NUMBER: _ClassVar[int]
    analyzers: _containers.RepeatedCompositeFieldContainer[DataTableAnalyzerConfiguration]
    capture_id: int
    export_columns: _containers.RepeatedScalarFieldContainer[str]
    filepath: str
    filter: DataTableFilter
    iso8601: bool
    def __init__(self, capture_id: _Optional[int] = ..., filepath: _Optional[str] = ..., analyzers: _Optional[_Iterable[_Union[DataTableAnalyzerConfiguration, _Mapping]]] = ..., iso8601: bool = ..., export_columns: _Optional[_Iterable[str]] = ..., filter: _Optional[_Union[DataTableFilter, _Mapping]] = ...) -> None: ...

class ExportRawDataBinaryReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ExportRawDataBinaryRequest(_message.Message):
    __slots__ = ["analog_downsample_ratio", "capture_id", "channels", "directory"]
    ANALOG_DOWNSAMPLE_RATIO_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    analog_downsample_ratio: int
    capture_id: int
    channels: _containers.RepeatedCompositeFieldContainer[ChannelIdentifier]
    directory: str
    def __init__(self, capture_id: _Optional[int] = ..., directory: _Optional[str] = ..., channels: _Optional[_Iterable[_Union[ChannelIdentifier, _Mapping]]] = ..., analog_downsample_ratio: _Optional[int] = ...) -> None: ...

class ExportRawDataCsvReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ExportRawDataCsvRequest(_message.Message):
    __slots__ = ["analog_downsample_ratio", "capture_id", "channels", "directory", "iso8601"]
    ANALOG_DOWNSAMPLE_RATIO_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    ISO8601_FIELD_NUMBER: _ClassVar[int]
    analog_downsample_ratio: int
    capture_id: int
    channels: _containers.RepeatedCompositeFieldContainer[ChannelIdentifier]
    directory: str
    iso8601: bool
    def __init__(self, capture_id: _Optional[int] = ..., directory: _Optional[str] = ..., channels: _Optional[_Iterable[_Union[ChannelIdentifier, _Mapping]]] = ..., analog_downsample_ratio: _Optional[int] = ..., iso8601: bool = ...) -> None: ...

class GetAppInfoReply(_message.Message):
    __slots__ = ["app_info"]
    APP_INFO_FIELD_NUMBER: _ClassVar[int]
    app_info: AppInfo
    def __init__(self, app_info: _Optional[_Union[AppInfo, _Mapping]] = ...) -> None: ...

class GetAppInfoRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetDevicesReply(_message.Message):
    __slots__ = ["devices"]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[Device]
    def __init__(self, devices: _Optional[_Iterable[_Union[Device, _Mapping]]] = ...) -> None: ...

class GetDevicesRequest(_message.Message):
    __slots__ = ["include_simulation_devices"]
    INCLUDE_SIMULATION_DEVICES_FIELD_NUMBER: _ClassVar[int]
    include_simulation_devices: bool
    def __init__(self, include_simulation_devices: bool = ...) -> None: ...

class GlitchFilterEntry(_message.Message):
    __slots__ = ["channel_index", "pulse_width_seconds"]
    CHANNEL_INDEX_FIELD_NUMBER: _ClassVar[int]
    PULSE_WIDTH_SECONDS_FIELD_NUMBER: _ClassVar[int]
    channel_index: int
    pulse_width_seconds: float
    def __init__(self, channel_index: _Optional[int] = ..., pulse_width_seconds: _Optional[float] = ...) -> None: ...

class LoadCaptureReply(_message.Message):
    __slots__ = ["capture_info"]
    CAPTURE_INFO_FIELD_NUMBER: _ClassVar[int]
    capture_info: CaptureInfo
    def __init__(self, capture_info: _Optional[_Union[CaptureInfo, _Mapping]] = ...) -> None: ...

class LoadCaptureRequest(_message.Message):
    __slots__ = ["filepath"]
    FILEPATH_FIELD_NUMBER: _ClassVar[int]
    filepath: str
    def __init__(self, filepath: _Optional[str] = ...) -> None: ...

class LogicDeviceConfiguration(_message.Message):
    __slots__ = ["analog_sample_rate", "digital_sample_rate", "digital_threshold_volts", "enabled_analog_channels", "enabled_digital_channels", "glitch_filters"]
    ANALOG_SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_THRESHOLD_VOLTS_FIELD_NUMBER: _ClassVar[int]
    ENABLED_ANALOG_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    ENABLED_DIGITAL_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    GLITCH_FILTERS_FIELD_NUMBER: _ClassVar[int]
    analog_sample_rate: int
    digital_sample_rate: int
    digital_threshold_volts: float
    enabled_analog_channels: _containers.RepeatedScalarFieldContainer[int]
    enabled_digital_channels: _containers.RepeatedScalarFieldContainer[int]
    glitch_filters: _containers.RepeatedCompositeFieldContainer[GlitchFilterEntry]
    def __init__(self, enabled_digital_channels: _Optional[_Iterable[int]] = ..., enabled_analog_channels: _Optional[_Iterable[int]] = ..., digital_sample_rate: _Optional[int] = ..., analog_sample_rate: _Optional[int] = ..., digital_threshold_volts: _Optional[float] = ..., glitch_filters: _Optional[_Iterable[_Union[GlitchFilterEntry, _Mapping]]] = ...) -> None: ...

class ManualCaptureMode(_message.Message):
    __slots__ = ["trim_data_seconds"]
    TRIM_DATA_SECONDS_FIELD_NUMBER: _ClassVar[int]
    trim_data_seconds: float
    def __init__(self, trim_data_seconds: _Optional[float] = ...) -> None: ...

class RemoveAnalyzerReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RemoveAnalyzerRequest(_message.Message):
    __slots__ = ["analyzer_id", "capture_id"]
    ANALYZER_ID_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    analyzer_id: int
    capture_id: int
    def __init__(self, capture_id: _Optional[int] = ..., analyzer_id: _Optional[int] = ...) -> None: ...

class SaveCaptureReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SaveCaptureRequest(_message.Message):
    __slots__ = ["capture_id", "filepath"]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    FILEPATH_FIELD_NUMBER: _ClassVar[int]
    capture_id: int
    filepath: str
    def __init__(self, capture_id: _Optional[int] = ..., filepath: _Optional[str] = ...) -> None: ...

class StartCaptureReply(_message.Message):
    __slots__ = ["capture_info"]
    CAPTURE_INFO_FIELD_NUMBER: _ClassVar[int]
    capture_info: CaptureInfo
    def __init__(self, capture_info: _Optional[_Union[CaptureInfo, _Mapping]] = ...) -> None: ...

class StartCaptureRequest(_message.Message):
    __slots__ = ["capture_configuration", "device_id", "logic_device_configuration"]
    CAPTURE_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    LOGIC_DEVICE_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    capture_configuration: CaptureConfiguration
    device_id: str
    logic_device_configuration: LogicDeviceConfiguration
    def __init__(self, device_id: _Optional[str] = ..., logic_device_configuration: _Optional[_Union[LogicDeviceConfiguration, _Mapping]] = ..., capture_configuration: _Optional[_Union[CaptureConfiguration, _Mapping]] = ...) -> None: ...

class StopCaptureReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class StopCaptureRequest(_message.Message):
    __slots__ = ["capture_id"]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    capture_id: int
    def __init__(self, capture_id: _Optional[int] = ...) -> None: ...

class TimedCaptureMode(_message.Message):
    __slots__ = ["duration_seconds", "trim_data_seconds"]
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TRIM_DATA_SECONDS_FIELD_NUMBER: _ClassVar[int]
    duration_seconds: float
    trim_data_seconds: float
    def __init__(self, duration_seconds: _Optional[float] = ..., trim_data_seconds: _Optional[float] = ...) -> None: ...

class Version(_message.Message):
    __slots__ = ["major", "minor", "patch"]
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    patch: int
    def __init__(self, major: _Optional[int] = ..., minor: _Optional[int] = ..., patch: _Optional[int] = ...) -> None: ...

class WaitCaptureReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class WaitCaptureRequest(_message.Message):
    __slots__ = ["capture_id"]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    capture_id: int
    def __init__(self, capture_id: _Optional[int] = ...) -> None: ...

class ThisApiVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class RadixType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DeviceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ChannelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DigitalTriggerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DigitalTriggerLinkedChannelState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
