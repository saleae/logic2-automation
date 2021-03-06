from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CHANNEL_TYPE_ANALOG: ChannelType
CHANNEL_TYPE_DIGITAL: ChannelType
CHANNEL_TYPE_UNSPECIFIED: ChannelType
DESCRIPTOR: _descriptor.FileDescriptor
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
ERROR_CODE_OOM: ErrorCode
ERROR_CODE_UNSPECIFIED: ErrorCode
RADIX_TYPE_ASCII: RadixType
RADIX_TYPE_BINARY: RadixType
RADIX_TYPE_DECIMAL: RadixType
RADIX_TYPE_HEXADECIMAL: RadixType
RADIX_TYPE_UNSPECIFIED: RadixType

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
    device_id: int
    index: int
    type: ChannelType
    def __init__(self, device_id: _Optional[int] = ..., type: _Optional[_Union[ChannelType, str]] = ..., index: _Optional[int] = ...) -> None: ...

class CloseCaptureReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CloseCaptureRequest(_message.Message):
    __slots__ = ["capture_id"]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    capture_id: int
    def __init__(self, capture_id: _Optional[int] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ["device_id", "device_type", "serial_number"]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    device_id: int
    device_type: DeviceType
    serial_number: str
    def __init__(self, device_id: _Optional[int] = ..., device_type: _Optional[_Union[DeviceType, str]] = ..., serial_number: _Optional[str] = ...) -> None: ...

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
    __slots__ = ["analyzer_ids", "capture_id", "filepath", "iso8601", "radix_type"]
    ANALYZER_IDS_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    FILEPATH_FIELD_NUMBER: _ClassVar[int]
    ISO8601_FIELD_NUMBER: _ClassVar[int]
    RADIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    analyzer_ids: _containers.RepeatedScalarFieldContainer[int]
    capture_id: int
    filepath: str
    iso8601: bool
    radix_type: RadixType
    def __init__(self, capture_id: _Optional[int] = ..., filepath: _Optional[str] = ..., analyzer_ids: _Optional[_Iterable[int]] = ..., iso8601: bool = ..., radix_type: _Optional[_Union[RadixType, str]] = ...) -> None: ...

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

class GetDevicesReply(_message.Message):
    __slots__ = ["devices"]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[Device]
    def __init__(self, devices: _Optional[_Iterable[_Union[Device, _Mapping]]] = ...) -> None: ...

class GetDevicesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

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
    __slots__ = ["capture_configuration", "device_serial_number", "logic_device_configuration"]
    CAPTURE_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LOGIC_DEVICE_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    capture_configuration: CaptureConfiguration
    device_serial_number: str
    logic_device_configuration: LogicDeviceConfiguration
    def __init__(self, device_serial_number: _Optional[str] = ..., logic_device_configuration: _Optional[_Union[LogicDeviceConfiguration, _Mapping]] = ..., capture_configuration: _Optional[_Union[CaptureConfiguration, _Mapping]] = ...) -> None: ...

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

class WaitCaptureReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class WaitCaptureRequest(_message.Message):
    __slots__ = ["capture_id"]
    CAPTURE_ID_FIELD_NUMBER: _ClassVar[int]
    capture_id: int
    def __init__(self, capture_id: _Optional[int] = ...) -> None: ...

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
