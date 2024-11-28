from concurrent import futures
import grpc
from admin.dao.mongoDAO import MongoDAO
from admin.grpc.admin_service_pb2 import (
    Response,
    FlaggedItemsResponse,
    ActiveAuctionsResponse,
    MetricsResponse,
)
from admin.consts.consts import *
import admin.grpc.admin_service_pb2_grpc as admin_service_pb2_grpc


class AdminService(admin_service_pb2_grpc.AdminServiceServicer):
    def __init__(self):
        self.dao = MongoDAO()

    def StopAuctionEarly(self, request, context):
        result = self.dao.stop_auction_early(request.auction_id)
        if result.modified_count:
            return Response(message="Auction stopped successfully.")
        return Response(message="Auction not found or already stopped.")

    def RemoveAndBlockUser(self, request, context):
        user_result, auction_count = self.dao.block_user_and_remove_auctions(request.user_id)
        if user_result:
            return Response(
                message=f"User blocked and {auction_count} auctions removed."
            )
        return Response(message="User not found.")

    def AddModifyRemoveCategory(self, request, context):
        if request.action == "add":
            self.dao.add_category(request.category_id, request.category_name)
            return Response(message="Category added.")
        elif request.action == "modify":
            result = self.dao.modify_category(request.category_id, request.category_name)
            if result.modified_count:
                return Response(message="Category modified.")
            return Response(message="Category not found.")
        elif request.action == "remove":
            result = self.dao.remove_category(request.category_id)
            if result.deleted_count:
                return Response(message="Category removed.")
            return Response(message="Category not found.")
        return Response(message="Invalid action.")

    def ViewFlaggedItems(self, request, context):
        flagged_items = self.dao.get_flagged_items()
        flagged_list = [item["_id"] for item in flagged_items]
        return FlaggedItemsResponse(flagged_items=flagged_list)

    def ViewActiveAuctions(self, request, context):
        auctions = self.dao.get_active_auctions(request.sort_by)
        auction_list = [auction["_id"] for auction in auctions]
        return ActiveAuctionsResponse(active_auctions=auction_list)

    def ExamineMetrics(self, request, context):
        closed_auctions = self.dao.get_closed_auctions_count(request.timeframe)
        return MetricsResponse(metrics={"closed_auctions": closed_auctions})

    def RespondToEmails(self, request, context):
        result = self.dao.respond_to_email(request.email_id, request.response_text)
        if result.modified_count:
            return Response(message="Email response sent.")
        return Response(message="Email not found.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    admin_service_pb2_grpc.add_AdminServiceServicer_to_server(AdminService(), server)
    server.add_insecure_port(f"[::]:{RPC_PORT}")
    print(f"Server started on port {RPC_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
