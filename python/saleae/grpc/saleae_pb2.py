# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: saleae/grpc/saleae.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18saleae/grpc/saleae.proto\x12\x11saleae.automation\"f\n\x06\x44\x65vice\x12\x11\n\tdevice_id\x18\x01 \x01(\x04\x12\x32\n\x0b\x64\x65vice_type\x18\x02 \x01(\x0e\x32\x1d.saleae.automation.DeviceType\x12\x15\n\rserial_number\x18\x03 \x01(\t\"c\n\x11\x43hannelIdentifier\x12\x11\n\tdevice_id\x18\x01 \x01(\x04\x12,\n\x04type\x18\x02 \x01(\x0e\x32\x1e.saleae.automation.ChannelType\x12\r\n\x05index\x18\x03 \x01(\x04\"!\n\x0b\x43\x61ptureInfo\x12\x12\n\ncapture_id\x18\x01 \x01(\x04\"\x13\n\x11GetDevicesRequest\"=\n\x0fGetDevicesReply\x12*\n\x07\x64\x65vices\x18\x01 \x03(\x0b\x32\x19.saleae.automation.Device\"\x9e\x01\n\x13StartCaptureRequest\x12\x1c\n\x14\x64\x65vice_serial_number\x18\x01 \x01(\t\x12Q\n\x1alogic_device_configuration\x18\x02 \x01(\x0b\x32+.saleae.automation.LogicDeviceConfigurationH\x00\x42\x16\n\x14\x64\x65vice_configuration\"I\n\x11StartCaptureReply\x12\x34\n\x0c\x63\x61pture_info\x18\x01 \x01(\x0b\x32\x1e.saleae.automation.CaptureInfo\"\xee\x01\n\x18LogicDeviceConfiguration\x12\x1f\n\x17\x65nabled_analog_channels\x18\x01 \x03(\r\x12 \n\x18\x65nabled_digital_channels\x18\x02 \x03(\r\x12\x1b\n\x13\x64igital_sample_rate\x18\x03 \x01(\r\x12\x1a\n\x12\x61nalog_sample_rate\x18\x04 \x01(\r\x12\x19\n\x11\x64igital_threshold\x18\x05 \x01(\x01\x12;\n\rglitch_filter\x18\x06 \x03(\x0b\x32$.saleae.automation.GlitchFilterEntry\"?\n\x11GlitchFilterEntry\x12\x15\n\rchannel_index\x18\x01 \x01(\r\x12\x13\n\x0bpulse_width\x18\x02 \x01(\x01\"(\n\x12StopCaptureRequest\x12\x12\n\ncapture_id\x18\x01 \x01(\x04\"\x12\n\x10StopCaptureReply\"&\n\x12LoadCaptureRequest\x12\x10\n\x08\x66ilepath\x18\x01 \x01(\t\"H\n\x10LoadCaptureReply\x12\x34\n\x0c\x63\x61pture_info\x18\x01 \x01(\x0b\x32\x1e.saleae.automation.CaptureInfo\":\n\x12SaveCaptureRequest\x12\x12\n\ncapture_id\x18\x01 \x01(\x04\x12\x10\n\x08\x66ilepath\x18\x02 \x01(\t\"\x12\n\x10SaveCaptureReply\")\n\x13\x43loseCaptureRequest\x12\x12\n\ncapture_id\x18\x01 \x01(\x04\"\x13\n\x11\x43loseCaptureReply\"\xaa\x01\n\x17\x45xportRawDataCsvRequest\x12\x12\n\ncapture_id\x18\x01 \x01(\x04\x12\x11\n\tdirectory\x18\x02 \x01(\t\x12\x36\n\x08\x63hannels\x18\x03 \x03(\x0b\x32$.saleae.automation.ChannelIdentifier\x12\x1f\n\x17\x61nalog_downsample_ratio\x18\x04 \x01(\x04\x12\x0f\n\x07iso8601\x18\x05 \x01(\x08\"\x17\n\x15\x45xportRawDataCsvReply\"\x9c\x01\n\x1a\x45xportRawDataBinaryRequest\x12\x12\n\ncapture_id\x18\x01 \x01(\x04\x12\x11\n\tdirectory\x18\x02 \x01(\t\x12\x36\n\x08\x63hannels\x18\x03 \x03(\x0b\x32$.saleae.automation.ChannelIdentifier\x12\x1f\n\x17\x61nalog_downsample_ratio\x18\x04 \x01(\x04\"\x1a\n\x18\x45xportRawDataBinaryReply*\xc8\x01\n\tErrorCode\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x16\n\x12INTERNAL_EXCEPTION\x10\x01\x12\x13\n\x0fINVALID_REQUEST\x10\n\x12\x17\n\x13LOAD_CAPTURE_FAILED\x10\x14\x12\x17\n\x13\x43\x41PTURE_IN_PROGRESS\x10\x15\x12\x19\n\x15UNSUPPORTED_FILE_TYPE\x10\x16\x12\x12\n\x0eMISSING_DEVICE\x10\x32\x12\x10\n\x0c\x44\x45VICE_ERROR\x10\x33\x12\x0e\n\nBACKLOGGED\x10\x34*U\n\nDeviceType\x12\x17\n\x13UNKNOWN_DEVICE_TYPE\x10\x00\x12\x0b\n\x07LOGIC_8\x10\x01\x12\x0f\n\x0bLOGIC_PRO_8\x10\x02\x12\x10\n\x0cLOGIC_PRO_16\x10\x03*&\n\x0b\x43hannelType\x12\x0b\n\x07\x44IGITAL\x10\x00\x12\n\n\x06\x41NALOG\x10\x01\x32\x9b\x06\n\x07Manager\x12X\n\nGetDevices\x12$.saleae.automation.GetDevicesRequest\x1a\".saleae.automation.GetDevicesReply\"\x00\x12^\n\x0cStartCapture\x12&.saleae.automation.StartCaptureRequest\x1a$.saleae.automation.StartCaptureReply\"\x00\x12[\n\x0bStopCapture\x12%.saleae.automation.StopCaptureRequest\x1a#.saleae.automation.StopCaptureReply\"\x00\x12[\n\x0bLoadCapture\x12%.saleae.automation.LoadCaptureRequest\x1a#.saleae.automation.LoadCaptureReply\"\x00\x12[\n\x0bSaveCapture\x12%.saleae.automation.SaveCaptureRequest\x1a#.saleae.automation.SaveCaptureReply\"\x00\x12^\n\x0c\x43loseCapture\x12&.saleae.automation.CloseCaptureRequest\x1a$.saleae.automation.CloseCaptureReply\"\x00\x12j\n\x10\x45xportRawDataCsv\x12*.saleae.automation.ExportRawDataCsvRequest\x1a(.saleae.automation.ExportRawDataCsvReply\"\x00\x12s\n\x13\x45xportRawDataBinary\x12-.saleae.automation.ExportRawDataBinaryRequest\x1a+.saleae.automation.ExportRawDataBinaryReply\"\x00\x42 \n\x06saleaeB\x0bSaleaeProtoP\x01\xa2\x02\x06Saleaeb\x06proto3')

_ERRORCODE = DESCRIPTOR.enum_types_by_name['ErrorCode']
ErrorCode = enum_type_wrapper.EnumTypeWrapper(_ERRORCODE)
_DEVICETYPE = DESCRIPTOR.enum_types_by_name['DeviceType']
DeviceType = enum_type_wrapper.EnumTypeWrapper(_DEVICETYPE)
_CHANNELTYPE = DESCRIPTOR.enum_types_by_name['ChannelType']
ChannelType = enum_type_wrapper.EnumTypeWrapper(_CHANNELTYPE)
UNKNOWN = 0
INTERNAL_EXCEPTION = 1
INVALID_REQUEST = 10
LOAD_CAPTURE_FAILED = 20
CAPTURE_IN_PROGRESS = 21
UNSUPPORTED_FILE_TYPE = 22
MISSING_DEVICE = 50
DEVICE_ERROR = 51
BACKLOGGED = 52
UNKNOWN_DEVICE_TYPE = 0
LOGIC_8 = 1
LOGIC_PRO_8 = 2
LOGIC_PRO_16 = 3
DIGITAL = 0
ANALOG = 1


_DEVICE = DESCRIPTOR.message_types_by_name['Device']
_CHANNELIDENTIFIER = DESCRIPTOR.message_types_by_name['ChannelIdentifier']
_CAPTUREINFO = DESCRIPTOR.message_types_by_name['CaptureInfo']
_GETDEVICESREQUEST = DESCRIPTOR.message_types_by_name['GetDevicesRequest']
_GETDEVICESREPLY = DESCRIPTOR.message_types_by_name['GetDevicesReply']
_STARTCAPTUREREQUEST = DESCRIPTOR.message_types_by_name['StartCaptureRequest']
_STARTCAPTUREREPLY = DESCRIPTOR.message_types_by_name['StartCaptureReply']
_LOGICDEVICECONFIGURATION = DESCRIPTOR.message_types_by_name['LogicDeviceConfiguration']
_GLITCHFILTERENTRY = DESCRIPTOR.message_types_by_name['GlitchFilterEntry']
_STOPCAPTUREREQUEST = DESCRIPTOR.message_types_by_name['StopCaptureRequest']
_STOPCAPTUREREPLY = DESCRIPTOR.message_types_by_name['StopCaptureReply']
_LOADCAPTUREREQUEST = DESCRIPTOR.message_types_by_name['LoadCaptureRequest']
_LOADCAPTUREREPLY = DESCRIPTOR.message_types_by_name['LoadCaptureReply']
_SAVECAPTUREREQUEST = DESCRIPTOR.message_types_by_name['SaveCaptureRequest']
_SAVECAPTUREREPLY = DESCRIPTOR.message_types_by_name['SaveCaptureReply']
_CLOSECAPTUREREQUEST = DESCRIPTOR.message_types_by_name['CloseCaptureRequest']
_CLOSECAPTUREREPLY = DESCRIPTOR.message_types_by_name['CloseCaptureReply']
_EXPORTRAWDATACSVREQUEST = DESCRIPTOR.message_types_by_name['ExportRawDataCsvRequest']
_EXPORTRAWDATACSVREPLY = DESCRIPTOR.message_types_by_name['ExportRawDataCsvReply']
_EXPORTRAWDATABINARYREQUEST = DESCRIPTOR.message_types_by_name['ExportRawDataBinaryRequest']
_EXPORTRAWDATABINARYREPLY = DESCRIPTOR.message_types_by_name['ExportRawDataBinaryReply']
Device = _reflection.GeneratedProtocolMessageType('Device', (_message.Message,), {
  'DESCRIPTOR' : _DEVICE,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.Device)
  })
_sym_db.RegisterMessage(Device)

ChannelIdentifier = _reflection.GeneratedProtocolMessageType('ChannelIdentifier', (_message.Message,), {
  'DESCRIPTOR' : _CHANNELIDENTIFIER,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.ChannelIdentifier)
  })
_sym_db.RegisterMessage(ChannelIdentifier)

CaptureInfo = _reflection.GeneratedProtocolMessageType('CaptureInfo', (_message.Message,), {
  'DESCRIPTOR' : _CAPTUREINFO,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.CaptureInfo)
  })
_sym_db.RegisterMessage(CaptureInfo)

GetDevicesRequest = _reflection.GeneratedProtocolMessageType('GetDevicesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETDEVICESREQUEST,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.GetDevicesRequest)
  })
_sym_db.RegisterMessage(GetDevicesRequest)

GetDevicesReply = _reflection.GeneratedProtocolMessageType('GetDevicesReply', (_message.Message,), {
  'DESCRIPTOR' : _GETDEVICESREPLY,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.GetDevicesReply)
  })
_sym_db.RegisterMessage(GetDevicesReply)

StartCaptureRequest = _reflection.GeneratedProtocolMessageType('StartCaptureRequest', (_message.Message,), {
  'DESCRIPTOR' : _STARTCAPTUREREQUEST,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.StartCaptureRequest)
  })
_sym_db.RegisterMessage(StartCaptureRequest)

StartCaptureReply = _reflection.GeneratedProtocolMessageType('StartCaptureReply', (_message.Message,), {
  'DESCRIPTOR' : _STARTCAPTUREREPLY,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.StartCaptureReply)
  })
_sym_db.RegisterMessage(StartCaptureReply)

LogicDeviceConfiguration = _reflection.GeneratedProtocolMessageType('LogicDeviceConfiguration', (_message.Message,), {
  'DESCRIPTOR' : _LOGICDEVICECONFIGURATION,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.LogicDeviceConfiguration)
  })
_sym_db.RegisterMessage(LogicDeviceConfiguration)

GlitchFilterEntry = _reflection.GeneratedProtocolMessageType('GlitchFilterEntry', (_message.Message,), {
  'DESCRIPTOR' : _GLITCHFILTERENTRY,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.GlitchFilterEntry)
  })
_sym_db.RegisterMessage(GlitchFilterEntry)

StopCaptureRequest = _reflection.GeneratedProtocolMessageType('StopCaptureRequest', (_message.Message,), {
  'DESCRIPTOR' : _STOPCAPTUREREQUEST,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.StopCaptureRequest)
  })
_sym_db.RegisterMessage(StopCaptureRequest)

StopCaptureReply = _reflection.GeneratedProtocolMessageType('StopCaptureReply', (_message.Message,), {
  'DESCRIPTOR' : _STOPCAPTUREREPLY,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.StopCaptureReply)
  })
_sym_db.RegisterMessage(StopCaptureReply)

LoadCaptureRequest = _reflection.GeneratedProtocolMessageType('LoadCaptureRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOADCAPTUREREQUEST,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.LoadCaptureRequest)
  })
_sym_db.RegisterMessage(LoadCaptureRequest)

LoadCaptureReply = _reflection.GeneratedProtocolMessageType('LoadCaptureReply', (_message.Message,), {
  'DESCRIPTOR' : _LOADCAPTUREREPLY,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.LoadCaptureReply)
  })
_sym_db.RegisterMessage(LoadCaptureReply)

SaveCaptureRequest = _reflection.GeneratedProtocolMessageType('SaveCaptureRequest', (_message.Message,), {
  'DESCRIPTOR' : _SAVECAPTUREREQUEST,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.SaveCaptureRequest)
  })
_sym_db.RegisterMessage(SaveCaptureRequest)

SaveCaptureReply = _reflection.GeneratedProtocolMessageType('SaveCaptureReply', (_message.Message,), {
  'DESCRIPTOR' : _SAVECAPTUREREPLY,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.SaveCaptureReply)
  })
_sym_db.RegisterMessage(SaveCaptureReply)

CloseCaptureRequest = _reflection.GeneratedProtocolMessageType('CloseCaptureRequest', (_message.Message,), {
  'DESCRIPTOR' : _CLOSECAPTUREREQUEST,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.CloseCaptureRequest)
  })
_sym_db.RegisterMessage(CloseCaptureRequest)

CloseCaptureReply = _reflection.GeneratedProtocolMessageType('CloseCaptureReply', (_message.Message,), {
  'DESCRIPTOR' : _CLOSECAPTUREREPLY,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.CloseCaptureReply)
  })
_sym_db.RegisterMessage(CloseCaptureReply)

ExportRawDataCsvRequest = _reflection.GeneratedProtocolMessageType('ExportRawDataCsvRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXPORTRAWDATACSVREQUEST,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.ExportRawDataCsvRequest)
  })
_sym_db.RegisterMessage(ExportRawDataCsvRequest)

ExportRawDataCsvReply = _reflection.GeneratedProtocolMessageType('ExportRawDataCsvReply', (_message.Message,), {
  'DESCRIPTOR' : _EXPORTRAWDATACSVREPLY,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.ExportRawDataCsvReply)
  })
_sym_db.RegisterMessage(ExportRawDataCsvReply)

ExportRawDataBinaryRequest = _reflection.GeneratedProtocolMessageType('ExportRawDataBinaryRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXPORTRAWDATABINARYREQUEST,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.ExportRawDataBinaryRequest)
  })
_sym_db.RegisterMessage(ExportRawDataBinaryRequest)

ExportRawDataBinaryReply = _reflection.GeneratedProtocolMessageType('ExportRawDataBinaryReply', (_message.Message,), {
  'DESCRIPTOR' : _EXPORTRAWDATABINARYREPLY,
  '__module__' : 'saleae.grpc.saleae_pb2'
  # @@protoc_insertion_point(class_scope:saleae.automation.ExportRawDataBinaryReply)
  })
_sym_db.RegisterMessage(ExportRawDataBinaryReply)

_MANAGER = DESCRIPTOR.services_by_name['Manager']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\006saleaeB\013SaleaeProtoP\001\242\002\006Saleae'
  _ERRORCODE._serialized_start=1619
  _ERRORCODE._serialized_end=1819
  _DEVICETYPE._serialized_start=1821
  _DEVICETYPE._serialized_end=1906
  _CHANNELTYPE._serialized_start=1908
  _CHANNELTYPE._serialized_end=1946
  _DEVICE._serialized_start=47
  _DEVICE._serialized_end=149
  _CHANNELIDENTIFIER._serialized_start=151
  _CHANNELIDENTIFIER._serialized_end=250
  _CAPTUREINFO._serialized_start=252
  _CAPTUREINFO._serialized_end=285
  _GETDEVICESREQUEST._serialized_start=287
  _GETDEVICESREQUEST._serialized_end=306
  _GETDEVICESREPLY._serialized_start=308
  _GETDEVICESREPLY._serialized_end=369
  _STARTCAPTUREREQUEST._serialized_start=372
  _STARTCAPTUREREQUEST._serialized_end=530
  _STARTCAPTUREREPLY._serialized_start=532
  _STARTCAPTUREREPLY._serialized_end=605
  _LOGICDEVICECONFIGURATION._serialized_start=608
  _LOGICDEVICECONFIGURATION._serialized_end=846
  _GLITCHFILTERENTRY._serialized_start=848
  _GLITCHFILTERENTRY._serialized_end=911
  _STOPCAPTUREREQUEST._serialized_start=913
  _STOPCAPTUREREQUEST._serialized_end=953
  _STOPCAPTUREREPLY._serialized_start=955
  _STOPCAPTUREREPLY._serialized_end=973
  _LOADCAPTUREREQUEST._serialized_start=975
  _LOADCAPTUREREQUEST._serialized_end=1013
  _LOADCAPTUREREPLY._serialized_start=1015
  _LOADCAPTUREREPLY._serialized_end=1087
  _SAVECAPTUREREQUEST._serialized_start=1089
  _SAVECAPTUREREQUEST._serialized_end=1147
  _SAVECAPTUREREPLY._serialized_start=1149
  _SAVECAPTUREREPLY._serialized_end=1167
  _CLOSECAPTUREREQUEST._serialized_start=1169
  _CLOSECAPTUREREQUEST._serialized_end=1210
  _CLOSECAPTUREREPLY._serialized_start=1212
  _CLOSECAPTUREREPLY._serialized_end=1231
  _EXPORTRAWDATACSVREQUEST._serialized_start=1234
  _EXPORTRAWDATACSVREQUEST._serialized_end=1404
  _EXPORTRAWDATACSVREPLY._serialized_start=1406
  _EXPORTRAWDATACSVREPLY._serialized_end=1429
  _EXPORTRAWDATABINARYREQUEST._serialized_start=1432
  _EXPORTRAWDATABINARYREQUEST._serialized_end=1588
  _EXPORTRAWDATABINARYREPLY._serialized_start=1590
  _EXPORTRAWDATABINARYREPLY._serialized_end=1616
  _MANAGER._serialized_start=1949
  _MANAGER._serialized_end=2744
# @@protoc_insertion_point(module_scope)
