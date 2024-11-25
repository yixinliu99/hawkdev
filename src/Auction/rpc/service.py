from concurrent import futures
import datetime
import os
import grpc
import celery
from Auction.celery.celery_config import make_celery_tasks, make_celery
from Auction.models.models import Auction
from Auction.dao.mongoDAO import MongoDao
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
            auction.create(self.dao)
            self.capp.send_task("start_auction_task", args=[auction.id], countdown=(auction.starting_time - datetime.datetime.now()).total_seconds())
            return service_pb2.AuctionResponse(success=True, message="Auction created successfully")
        except Exception as e:
            # rollback
            auction.delete_from_db()
            return service_pb2.AuctionResponse(success=False, message=str(e))




    def UpdateAuction(self, request, context):
        # get auction by id
        try:
            auction = Auction.filter({"id": request.auction_id}, self.dao)
        except Exception as e:
            return service_pb2.AuctionResponse(success=False, message=str(e))

        # update auction
        try:
            auction.update(request.from_dict())
            return service_pb2.AuctionResponse(success=True, message="Auction updated successfully")
        except Exception as e:
            return service_pb2.AuctionResponse(success=False, message=str(e))



    def StartAuction(self, request, context):
        # get auction by id
        try:
            auction = Auction.filter({"id": request.auction_id}, self.dao)
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


def start_server(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dao = MongoDao()
    capp = make_celery("amqp://guest:guest@localhost:5672//")
    make_celery_tasks(capp)
    service_pb2_grpc.add_AuctionServiceServicer_to_server(AuctionService(dao, capp), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    if os.environ.get("AUCTION_SERVICE_PORT"):
        start_server(os.environ.get("AUCTION_SERVICE_PORT"))
    else:
        start_server(45671)
