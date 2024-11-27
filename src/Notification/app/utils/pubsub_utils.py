import json
from google.protobuf.json_format import Parse

def parse_pubsub_message(pubsub_message):
    message_data = json.loads(pubsub_message.data.decode('utf-8'))
    notification_message = NotificationMessage()
    Parse(message_data, notification_message)
    return notification_message
