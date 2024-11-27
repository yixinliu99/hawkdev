from google.protobuf import message
import datetime

class NotificationMessage(message.Message):
    user_id = message.Field('string', 1)
    item_id = message.Field('string', 2)
    body = message.Field('string', 3)
    timestamp = message.Field('string', 4, default=str(datetime.datetime.utcnow()))
