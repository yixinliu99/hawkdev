# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: user.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'user.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\"\x1e\n\x0bUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"\x1f\n\x0cUserResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"<\n\x03\x42id\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x12\n\nbid_amount\x18\x02 \x01(\x02\x12\x10\n\x08\x62id_time\x18\x03 \x01(\t\"\xb9\x01\n\x07\x41uction\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x16\n\x0estarting_price\x18\x02 \x01(\x02\x12\x15\n\rstarting_time\x18\x03 \x01(\t\x12\x13\n\x0b\x65nding_time\x18\x04 \x01(\t\x12\x11\n\tseller_id\x18\x05 \x01(\t\x12\x0f\n\x07item_id\x18\x06 \x01(\t\x12\x0e\n\x06\x61\x63tive\x18\x07 \x01(\x08\x12\x15\n\rcurrent_price\x18\x08 \x01(\x02\x12\x12\n\x04\x62ids\x18\t \x03(\x0b\x32\x04.Bid\"~\n\x14\x43reateAuctionRequest\x12\x16\n\x0estarting_price\x18\x01 \x01(\x02\x12\x15\n\rstarting_time\x18\x02 \x01(\t\x12\x13\n\x0b\x65nding_time\x18\x03 \x01(\t\x12\x11\n\tseller_id\x18\x04 \x01(\t\x12\x0f\n\x07item_id\x18\x05 \x01(\t\"M\n\x15\x43reateAuctionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x12\n\nauction_id\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"\x92\x01\n\x14UpdateAuctionRequest\x12\x12\n\nauction_id\x18\x01 \x01(\t\x12\x16\n\x0estarting_price\x18\x02 \x01(\x02\x12\x15\n\rstarting_time\x18\x03 \x01(\t\x12\x13\n\x0b\x65nding_time\x18\x04 \x01(\t\x12\x11\n\tseller_id\x18\x05 \x01(\t\x12\x0f\n\x07item_id\x18\x06 \x01(\t\"Q\n\x15UpdateAuctionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x16\n\x0emodified_count\x18\x02 \x01(\r\x12\x0f\n\x07message\x18\x03 \x01(\t\")\n\x13StartAuctionRequest\x12\x12\n\nauction_id\x18\x01 \x01(\t\"L\n\x14StartAuctionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x12\n\nauction_id\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"(\n\x12StopAuctionRequest\x12\x12\n\nauction_id\x18\x01 \x01(\t\"K\n\x13StopAuctionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x12\n\nauction_id\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"J\n\x0fPlaceBidRequest\x12\x12\n\nauction_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x12\n\nbid_amount\x18\x03 \x01(\x02\"H\n\x10PlaceBidResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x12\n\nauction_id\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"\"\n\x11GetAuctionRequest\x12\r\n\x05query\x18\x01 \x01(\t\"R\n\x12GetAuctionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x1a\n\x08\x61uctions\x18\x02 \x03(\x0b\x32\x08.Auction\x12\x0f\n\x07message\x18\x03 \x01(\t2\xf0\x02\n\x0e\x41uctionService\x12>\n\rCreateAuction\x12\x15.CreateAuctionRequest\x1a\x16.CreateAuctionResponse\x12>\n\rUpdateAuction\x12\x15.UpdateAuctionRequest\x1a\x16.UpdateAuctionResponse\x12;\n\x0cStartAuction\x12\x14.StartAuctionRequest\x1a\x15.StartAuctionResponse\x12\x38\n\x0bStopAuction\x12\x13.StopAuctionRequest\x1a\x14.StopAuctionResponse\x12/\n\x08PlaceBid\x12\x10.PlaceBidRequest\x1a\x11.PlaceBidResponse\x12\x36\n\x0bGetAuctions\x12\x12.GetAuctionRequest\x1a\x13.GetAuctionResponse2@\n\x0bUserService\x12\x31\n\x12RemoveAndBlockUser\x12\x0c.UserRequest\x1a\r.UserResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_USERREQUEST']._serialized_start=14
  _globals['_USERREQUEST']._serialized_end=44
  _globals['_USERRESPONSE']._serialized_start=46
  _globals['_USERRESPONSE']._serialized_end=77
  _globals['_BID']._serialized_start=79
  _globals['_BID']._serialized_end=139
  _globals['_AUCTION']._serialized_start=142
  _globals['_AUCTION']._serialized_end=327
  _globals['_CREATEAUCTIONREQUEST']._serialized_start=329
  _globals['_CREATEAUCTIONREQUEST']._serialized_end=455
  _globals['_CREATEAUCTIONRESPONSE']._serialized_start=457
  _globals['_CREATEAUCTIONRESPONSE']._serialized_end=534
  _globals['_UPDATEAUCTIONREQUEST']._serialized_start=537
  _globals['_UPDATEAUCTIONREQUEST']._serialized_end=683
  _globals['_UPDATEAUCTIONRESPONSE']._serialized_start=685
  _globals['_UPDATEAUCTIONRESPONSE']._serialized_end=766
  _globals['_STARTAUCTIONREQUEST']._serialized_start=768
  _globals['_STARTAUCTIONREQUEST']._serialized_end=809
  _globals['_STARTAUCTIONRESPONSE']._serialized_start=811
  _globals['_STARTAUCTIONRESPONSE']._serialized_end=887
  _globals['_STOPAUCTIONREQUEST']._serialized_start=889
  _globals['_STOPAUCTIONREQUEST']._serialized_end=929
  _globals['_STOPAUCTIONRESPONSE']._serialized_start=931
  _globals['_STOPAUCTIONRESPONSE']._serialized_end=1006
  _globals['_PLACEBIDREQUEST']._serialized_start=1008
  _globals['_PLACEBIDREQUEST']._serialized_end=1082
  _globals['_PLACEBIDRESPONSE']._serialized_start=1084
  _globals['_PLACEBIDRESPONSE']._serialized_end=1156
  _globals['_GETAUCTIONREQUEST']._serialized_start=1158
  _globals['_GETAUCTIONREQUEST']._serialized_end=1192
  _globals['_GETAUCTIONRESPONSE']._serialized_start=1194
  _globals['_GETAUCTIONRESPONSE']._serialized_end=1276
  _globals['_AUCTIONSERVICE']._serialized_start=1279
  _globals['_AUCTIONSERVICE']._serialized_end=1647
  _globals['_USERSERVICE']._serialized_start=1649
  _globals['_USERSERVICE']._serialized_end=1713
# @@protoc_insertion_point(module_scope)