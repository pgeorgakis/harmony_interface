# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: start_ofs.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fstart_ofs.proto\x12\rharmonyServer\"\xe2\x05\n\x08StartOFS\x12\x12\n\nscenarioId\x18\x01 \x02(\t\x12.\n\x06inputs\x18\x02 \x02(\x0b\x32\x1e.harmonyServer.StartOFS.Inputs\x12\x30\n\x07outputs\x18\x03 \x02(\x0b\x32\x1f.harmonyServer.StartOFS.Outputs\x1a\xc0\x04\n\x06Inputs\x12\x0e\n\x06\x44\x42Host\x18\x01 \x02(\t\x12\x0e\n\x06\x44\x42Port\x18\x02 \x02(\x05\x12\r\n\x05\x44\x42SSL\x18\x03 \x01(\x08\x12\x18\n\x10\x44\x42\x41uthentication\x18\x04 \x01(\x08\x12\x1e\n\x16\x44\x42\x41uthenticationSource\x18\x05 \x01(\t\x12\x1c\n\x14\x44\x42\x41uthenticationType\x18\x06 \x01(\t\x12 \n\x18\x44\x42\x41uthenticationUserName\x18\x07 \x01(\t\x12 \n\x18\x44\x42\x41uthenticationPassword\x18\x08 \x01(\t\x12\x14\n\x0c\x44\x61tabaseName\x18\t \x01(\t\x12\x17\n\x0fNodesCollection\x18\n \x01(\t\x12\x17\n\x0fLinksCollection\x18\x0b \x01(\t\x12\x17\n\x0fZonesCollection\x18\x0c \x01(\t\x12&\n\x1e\x43onsolidationCentresCollection\x18\r \x02(\t\x12\x1b\n\x13MicrohubsCollection\x18\x0e \x02(\t\x12\x1e\n\x16ParcelDemandCollection\x18\x0f \x02(\t\x12!\n\x19ShipmentsDemandCollection\x18\x10 \x01(\t\x12 \n\x18ShipmentsToursCollection\x18\x11 \x01(\t\x12\x1d\n\x15ParcelToursCollection\x18\x12 \x01(\t\x12!\n\x19TravelTimesSkimCollection\x18\x13 \x01(\t\x12\x1e\n\x16\x44istanceSkimCollection\x18\x14 \x01(\t\x1a\x1d\n\x07Outputs\x12\x12\n\nOFSResults\x18\x01 \x02(\t')



_STARTOFS = DESCRIPTOR.message_types_by_name['StartOFS']
_STARTOFS_INPUTS = _STARTOFS.nested_types_by_name['Inputs']
_STARTOFS_OUTPUTS = _STARTOFS.nested_types_by_name['Outputs']
StartOFS = _reflection.GeneratedProtocolMessageType('StartOFS', (_message.Message,), {

  'Inputs' : _reflection.GeneratedProtocolMessageType('Inputs', (_message.Message,), {
    'DESCRIPTOR' : _STARTOFS_INPUTS,
    '__module__' : 'start_ofs_pb2'
    # @@protoc_insertion_point(class_scope:harmonyServer.StartOFS.Inputs)
    })
  ,

  'Outputs' : _reflection.GeneratedProtocolMessageType('Outputs', (_message.Message,), {
    'DESCRIPTOR' : _STARTOFS_OUTPUTS,
    '__module__' : 'start_ofs_pb2'
    # @@protoc_insertion_point(class_scope:harmonyServer.StartOFS.Outputs)
    })
  ,
  'DESCRIPTOR' : _STARTOFS,
  '__module__' : 'start_ofs_pb2'
  # @@protoc_insertion_point(class_scope:harmonyServer.StartOFS)
  })
_sym_db.RegisterMessage(StartOFS)
_sym_db.RegisterMessage(StartOFS.Inputs)
_sym_db.RegisterMessage(StartOFS.Outputs)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STARTOFS._serialized_start=35
  _STARTOFS._serialized_end=773
  _STARTOFS_INPUTS._serialized_start=166
  _STARTOFS_INPUTS._serialized_end=742
  _STARTOFS_OUTPUTS._serialized_start=744
  _STARTOFS_OUTPUTS._serialized_end=773
# @@protoc_insertion_point(module_scope)