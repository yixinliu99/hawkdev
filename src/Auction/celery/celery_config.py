from celery import Celery
from Auction.dao.mongoDAO import MongoDao

def make_celery(broker_url):
    celery_app = Celery(
        "auction_tasks",
        broker=broker_url,
    )

    celery_app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
    )

    return celery_app

def make_celery_tasks(celery_app):
    @celery_app.task
    def start_auction_task(auction_id):
        dao = MongoDao()  # Initialize DAO
        auction = dao.get_auction_by_id(auction_id)  # Fetch auction by ID
        if auction:
            auction["status"] = "active"  # Update status to "active"
            dao.update_auction(auction_id, auction)  # Save updated auction
            return f"Auction {auction_id} started successfully"
        else:
            return f"Auction {auction_id} not found"
