import os

RABBITMQ_URI = os.getenv("RABBITMQ_URI", "amqp://guest@localhost:5672")
NOTIFY_EMAIL_HOST = os.getenv("NOTIFY_EMAIL_HOST", "smtp.gmail.com")
NOTIFY_EMAIL_PORT = os.getenv("NOTIFY_EMAIL_PORT", 587)
NOTIFY_EMAIL_USERNAME = os.getenv("NOTIFY_EMAIL_USERNAME", "vyshnavik0811@gmail.com")
NOTIFY_EMAIL_PASSWORD = os.getenv("NOTIFY_EMAIL_PASSWORD", "your-app-password")

AUCTION_SERVICE_PORT = os.getenv("AUCTION_SERVICE_PORT", 50051)
