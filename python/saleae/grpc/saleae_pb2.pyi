from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

ANALOG: ChannelType
CAPTURE_IN_PROGRESS: ErrorCode
DESCRIPTOR: _descriptor.FileDescriptor
DIGITAL: ChannelType
INTERNAL_EXCEPTION: ErrorCode
INVALID_REQUEST: ErrorCode
LOAD_CAPTURE_FAILED: ErrorCode
LOGIC_8: DeviceType
LOGIC_PRO_16: DeviceType
LOGIC_PRO_8: DeviceType
UNKNOWN: ErrorCode
UNKNOWN_DEVICE_TYPE: DeviceType
UNSUPPORTED_FILE_TYPE: ErrorCode

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

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DeviceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ChannelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
