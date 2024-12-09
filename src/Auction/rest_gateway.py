from flask import Flask, request, jsonify
from flask_cors import CORS
import grpc
import service_pb2
import service_pb2_grpc

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to gRPC service
channel = grpc.insecure_channel('localhost:50010')
stub = service_pb2_grpc.AuctionServiceStub(channel)

@app.route('/auctions/<auction_id>', methods=['GET'])
def get_auction(auction_id):
    try:
        query = {"_id": auction_id}
        json_query = json.dumps(query)
        get_request = service_pb2.GetAuctionRequest(query=json_query)
        get_response = stub.GetAuctions(get_request)
        return jsonify(get_response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/bids', methods=['POST'])
def place_bid():
    try:
        data = request.get_json()
        bid_request = service_pb2.PlaceBidRequest(
            auction_id=data['auction_id'],
            user_id=data['user_id'],
            bid_amount=data['bid_amount']
        )
        bid_response = stub.PlaceBid(bid_request)
        return jsonify(bid_response), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)