from concurrent import futures
import grpc
import src.Auction.db.mongoDbManager as mdb

import service_pb2
import service_pb2_grpc
from Auction.models import Auction


class AuctionService(service_pb2_grpc.AuctionService):
    def CreateAuction(self, request, context):
        auction = Auction(
            starting_price=request.starting_price,
            starting_time=request.starting_time,
            ending_time=request.ending_time,
            seller_id=request.seller_id,
            item_id=request.item_id,
            bids=[]
        )

        mdb.insert_auction(auction)

    def UpdateAuction(self, request, context):
        pass

    def StartAuction(self, request, context):
        pass

    def StopAuction(self, request, context):
        pass

    def PlaceBid(self, request, context):
        pass

    def SetAuctionWindow(self, request, context):
        pass

    def GetAuction(self, request, context):
        pass


def start_grpc_server(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_AuctionServiceServicer_to_server(AuctionService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()