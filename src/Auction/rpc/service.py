import datetime
import os
from concurrent import futures

import celery
import grpc
from bson import ObjectId

from Auction.celery.celery_config import make_celery_tasks, make_celery
from Auction.dao.mongoDAO import MongoDao
from Auction.models.auction import Auction
from Auction.rpc import service_pb2, service_pb2_grpc


class AuctionService(service_pb2_grpc.AuctionServiceServicer):
    def __init__(self, dao: MongoDao, capp: celery.Celery):
        self.dao = dao
        self.capp = capp

    def CreateAuction(self, request, context):
        auction = Auction(starting_price=request.starting_price, starting_time=request.starting_time,
                          ending_time=request.ending_time, item_id=request.item_id, seller_id=request.seller_id,
                          current_price=request.starting_price, bids=[])

        # schedule auction to start at starting_time
        try:
            auction_id = auction.create(self.dao)[0]
            self.capp.send_task("start_auction_task", args=[auction.id, self.dao],
                                countdown=(auction.starting_time - datetime.datetime.now()).total_seconds())
            return service_pb2.CreateAuctionResponse(success=True, auction_id=auction_id)
        except Exception as e:
            # rollback
            auction.delete(self.dao)
            return service_pb2.CreateAuctionResponse(success=False, auction_id=auction.id)

    def UpdateAuction(self, request, context):
        # get auction by id
        try:
            auction = Auction.filter({"_id": ObjectId(request.auction_id)}, self.dao)
        except Exception as e:
            return service_pb2.UpdateAuctionResponse(success=False, modified_count=0)

        # update auction
        try:
            modified_count = auction.update(self.dao)
            return service_pb2.UpdateAuctionResponse(success=True, modified_count=modified_count)
        except Exception as e:
            return service_pb2.UpdateAuctionResponse(success=False, modified_count=0)

    def StartAuction(self, request, context):
        # get auction by id
        try:
            auction = Auction.filter({"_id": ObjectId(request.auction_id)}, self.dao)
        except Exception as e:
            return service_pb2.AuctionResponse(success=False, message=str(e))

        # start auction
        try:
            auction.start_auction()
            return service_pb2.AuctionResponse(success=True, message="Auction started successfully")
        except Exception as e:
            return service_pb2.AuctionResponse(success=False, message=str(e))

    def StopAuction(self, request, context):
        # get auction by id
        try:
            auction = Auction.filter({"id": request.auction_id}, self.dao)
        except Exception as e:
            return service_pb2.AuctionResponse(success=False, message=str(e))

        # stop auction
        try:
            auction.stop_auction()
            return service_pb2.AuctionResponse(success=True, message="Auction stopped successfully")
        except Exception as e:
            return service_pb2.AuctionResponse(success=False, message=str(e))

    def PlaceBid(self, request, context):
        pass

    def SetAuctionWindow(self, request, context):
        pass

    def GetAuction(self, request, context):
        pass


def start_server(rpc_port, rabbitmq_port):
    dao = MongoDao()
    capp = make_celery(f"amqp://guest:guest@localhost:{rabbitmq_port}", dao)
    make_celery_tasks(capp)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port(f"[::]:{rpc_port}")
    service_pb2_grpc.add_AuctionServiceServicer_to_server(AuctionService(dao, capp), server)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    auction_service_rpc_server_port = int(os.environ.get("AUCTION_SERVICE_PORT"))
    auction_service_rabbitmq_port = int(os.environ.get("AUCTION_SERVICE_RABBITMQ_PORT"))
    start_server(auction_service_rpc_server_port, auction_service_rabbitmq_port)
