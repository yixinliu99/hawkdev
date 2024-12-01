import grpc
from app import user_pb2
from app import user_pb2_grpc
import json

def get_user_bids_from_auction(user_id):
    """Fetch active auctions where the user has placed bids."""
    with grpc.insecure_channel('localhost:50010') as channel:  # Auction Microservice gRPC server
        stub = user_pb2_grpc.AuctionServiceStub(channel)

        # Prepare the query to search for auctions where this user has placed a bid
        query = {"bids.user_id": user_id, "active": True}
        query_json = json.dumps(query)
        get_request = user_pb2.GetAuctionRequest(query=query_json)

        try:
            response = stub.GetAuctions(get_request)
            if response.success:
                return response.auctions  # Return the list of auctions
            else:
                return None  # Return None if no auctions are found or there's an error
        except grpc.RpcError as e:
            print(f"Error calling GetAuctions: {e}")
            return None
