from app.pubsub.pubsub_client import PubSubClient
from app.services.email import send_email_notification
from app.models import Watchlist, User
from app import db
import json

pubsub_client = PubSubClient(project_id="your-gcp-project-id")

def handle_event(message):
    event_data = json.loads(message.data.decode("utf-8"))

    if event_data["type"] == "new_bid":
        handle_new_bid(event_data)
    elif event_data["type"] == "item_available":
        handle_item_available(event_data)

def handle_new_bid(event_data):
    user_id = event_data["user_id"]
    item_id = event_data["item_id"]
    bid_amount = event_data["bid_amount"]

    user = User.get_by_id(user_id)
    if user:
        item_name = f"Item #{item_id}" 
        send_email_notification(user, item_name, f"A new bid of {bid_amount} has been placed.")

def handle_item_available(event_data):
    user_id = event_data["user_id"]
    item_id = event_data["item_id"]

    user = User.get_by_id(user_id)
    if user:
        item_name = f"Item #{item_id}"  
        send_email_notification(user, item_name, "The item you're watching is now available!")

def subscribe_to_events():
    pubsub_client.subscribe_to_topic("auction-events", handle_event)
    pubsub_client.subscribe_to_topic("watchlist-events", handle_event)
