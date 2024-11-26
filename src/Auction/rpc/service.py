import datetime
import os
from concurrent import futures

import celery
import grpc
from bson import ObjectId
from google.protobuf.json_format import (MessageToDict, )

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
        # create auction
        try:
            auction_id = auction.create(self.dao)[0]
        except Exception as e:
            # rollback
            auction.delete(self.dao)
            return service_pb2.CreateAuctionResponse(success=False, auction_id=auction.id, message=str(e))

        # schedule auction to start at starting_time
        try:
            self.capp.send_task("start_auction_task", args=[auction.id, self.dao],
                                countdown=(auction.starting_time - datetime.datetime.now()).total_seconds())

            return service_pb2.CreateAuctionResponse(success=True, auction_id=auction_id, message="")
        except Exception as e:
            # rollback
            auction.delete(self.dao)
            return service_pb2.CreateAuctionResponse(success=False, auction_id=auction.id, message=str(e))

    def UpdateAuction(self, request, context):
        try:
            if not isinstance(request.auction_id, ObjectId):
                auction_id = ObjectId(request.auction_id)
            else:
                auction_id = request.auction_id
            auction = Auction.filter({"_id": auction_id}, self.dao)[0]
            # update auction
            auction_dict = auction.to_dict()
            msg_dict = MessageToDict(request, preserving_proto_field_name=True)
            del msg_dict["auction_id"]
            for key, value in msg_dict.items():
                if key in auction_dict:
                    auction_dict[key] = value
                else:
                    return service_pb2.UpdateAuctionResponse(success=False, modified_count=0,
                                                             message="Invalid field: " + key)
            auction = Auction.from_dict(auction_dict)
            modified_count = auction.update(self.dao)
        except Exception as e:
            return service_pb2.UpdateAuctionResponse(success=False, modified_count=0, message=str(e))

        # schedule auction to start at starting_time
        try:
            self.capp.send_task("start_auction_task", args=[auction_id, self.dao],
                                countdown=(auction.starting_time - datetime.datetime.now()).total_seconds())

            return service_pb2.UpdateAuctionResponse(success=True, modified_count=modified_count, message="")
        except Exception as e:
            # rollback
            auction.delete(self.dao)
            return service_pb2.UpdateAuctionResponse(success=False, modified_count=0, message=str(e))

    def StartAuction(self, request, context):
        try:
            if not isinstance(request.auction_id, ObjectId):
                auction_id = ObjectId(request.auction_id)
            else:
                auction_id = request.auction_id
            auction = Auction.filter({"_id": auction_id}, self.dao)[0]
            auction.start_auction(self.dao)
            return service_pb2.StartAuctionResponse(success=True, message="")
        except Exception as e:
            return service_pb2.StartAuctionResponse(success=False, message=str(e))

    def StopAuction(self, request, context):
        try:
            if not isinstance(request.auction_id, ObjectId):
                auction_id = ObjectId(request.auction_id)
            else:
                auction_id = request.auction_id
            auction = Auction.filter({"_id": auction_id}, self.dao)[0]
            auction.stop_auction(self.dao)
            return service_pb2.StopAuctionResponse(success=True, message="")
        except Exception as e:
            return service_pb2.StopAuctionResponse(success=False, message=str(e))

    def PlaceBid(self, request, context):
        try:
            if not isinstance(request.auction_id, ObjectId):
                auction_id = ObjectId(request.auction_id)
            else:
                auction_id = request.auction_id
            auction = Auction.filter({"_id": auction_id}, self.dao)[0]
            auction.place_bid(request.user_id, request.bid_amount, self.dao)
            return service_pb2.PlaceBidResponse(success=True, message="")
        except Exception as e:
            return service_pb2.PlaceBidResponse(success=False, message=str(e))

    def GetAuction(self, request, context):
        try:
            query = request.query
            auctions = Auction.filter(query, self.dao)
            auctions_dict = [auction.to_dict() for auction in auctions]
            return service_pb2.GetAuctionResponse(auctions=auctions_dict)
        except Exception as e:
            return service_pb2.GetAuctionResponse(auctions=[], message=str(e))


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
