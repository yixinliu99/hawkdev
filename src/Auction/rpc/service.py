from concurrent import futures
import grpc
import src.Auction.db.mongoDbManager as mdb

import service_pb2
import service_pb2_grpc

class AuctionService(service_pb2_grpc.AuctionService):
    def CreateAuction(self, request, context):
        pass

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