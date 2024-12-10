import pika
import json
import logging
from app.notifications import send_email
from config.config import RABBITMQ_URI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def callback(ch, method, properties, body):
    logger.info(f"Received message: {body}")
    try:
        message = json.loads(body)
        event_type = message.get("event_type")
        logger.info(f"Processing event type: {event_type}")

        if event_type == "item_watchlist_match":
            user_email = message.get("user_email")
            keyword = message.get("keyword")
            category = message.get("category")
            send_email(user_email, "Item Matched Watchlist", f"The keyword '{keyword}', category '{category}' matches your criteria.")

        elif event_type == "new_bid_on_item":
            seller_email = message.get("seller_email")
            item_name = message.get("item_description")
            send_email(seller_email, "New Bid Placed", f"A bid has been placed on your item '{item_name}'.")

        elif event_type == "higher_bid":
            buyer_email = message.get("user_email")
            item_name = message.get("item_description")
            send_email(buyer_email, "Higher Bid Alert", f"A higher bid has been placed on your item '{item_name}'.")

        elif event_type == "auction_time_alert":
            seller_email = message.get("seller_email")
            bidders_emails = message.get("bidders_emails")
            item_description = message.get("item_description")
            time_left = message.get("time_left")
            send_email(seller_email, f"Time Alert for {item_description}", f"Your auction for '{item_description}' ends in {time_left}.")
            for email in bidders_emails:
                send_email(email, f"Time Alert for {item_description}", f"The auction for '{item_description}' ends in {time_left}.")

    except json.JSONDecodeError:
        logger.error("Failed to decode message body as JSON.")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def listen_for_events():
    try:
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URI))
        channel = connection.channel()

        channel.queue_declare(queue='auction_notifications', durable=True)
        channel.basic_consume(queue='auction_notifications', on_message_callback=callback, auto_ack=True)

        logger.info('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"RabbitMQ connection error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")
