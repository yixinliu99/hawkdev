from google.cloud import pubsub_v1
import json

class PubSubClient:
    def __init__(self, project_id):
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.project_id = project_id

    def publish_event(self, topic_name, event_data):
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        
        event_data_json = json.dumps(event_data).encode("utf-8")
        
        future = self.publisher.publish(topic_path, event_data_json)
        return future.result()

    def subscribe_to_topic(self, subscription_name, callback):
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)

        def message_callback(message):
            callback(message)
            message.ack()
        self.subscriber.subscribe(subscription_path, callback=message_callback)
