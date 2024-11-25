from celery import Celery
from Auction.models.auction import Auction

def make_celery(broker_url, service_rpc_server_port):
    celery_app = Celery(
        "auction_tasks",
        broker=broker_url,
        service_rpc_server_port=service_rpc_server_port
    )

    celery_app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True
    )



    return celery_app

def make_celery_tasks(celery_app):
    @celery_app.task
    def start_auction_task(auction_id, dao):
        auction = Auction.filter({"id": auction_id}, dao)
        auction.start_auction()
        auction.update(dao)

        return True
