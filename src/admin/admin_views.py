from flask import Flask, request, jsonify, render_template
import grpc
import admin.admin_rpc.admin_service_pb2 as admin_service_pb2
import admin.admin_rpc.admin_service_pb2_grpc as admin_service_pb2_grpc
import Auction.rpc.service_pb2 as service_pb2
import Auction.rpc.service_pb2_grpc as service_pb2_grpc
import User.app.grpc.user_pb2 as user_pb2
import User.app.grpc.user_pb2_grpc as user_pb2_grpc
from google.protobuf.json_format import MessageToJson
import json
from datetime import datetime, timedelta
from bson import ObjectId

import requests

app = Flask(__name__)

# gRPC connection setup
def get_grpc_stub():
    channel = grpc.insecure_channel("localhost:50051")  # Connect to the gRPC server
    return service_pb2_grpc.AuctionServiceStub(channel)

def get_user_grpc_stub():
    channel = grpc.insecure_channel("localhost:50053")  # Connect to the gRPC server
    return user_pb2_grpc.UserServiceStub(channel)

def auction_to_dict(auction):
    bids = bids_to_list(auction.bids)
    return {"_id": str(auction._id), "item_id": auction.item_id, "seller_id": auction.seller_id, "active": auction.active,
            "starting_time": auction.starting_time,
            "ending_time": auction.ending_time, "starting_price": auction.starting_price,
            "current_price": auction.current_price, "bids": bids,
            "buy_now_price": auction.buy_now_price if auction.buy_now_price else None}

def bids_to_list(bids):
    bid_list = []
    for bid in bids:
        temp = {
            "user_id": bid.user_id,
            "bid_amount": bid.bid_amount,
            "bid_time": bid.time
        }
        bid_list.append(temp)

    return bid_list


@app.route("/")
def index():
    return render_template("index.html")


# API Route: Stop an auction early
@app.route("/api/stop-auction", methods=["POST"])
def stop_auction():
    try:
        auction_id = request.json.get("auction_id")
        if not auction_id:
            return jsonify({"error": "auction_id is required"}), 400

        stub = get_grpc_stub()
        stop_request = service_pb2.StopAuctionRequest(auction_id=auction_id)
        stop_response = stub.StopAuction(stop_request)
        return jsonify({"message": stop_response.message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Route: Remove and block a user
@app.route("/api/remove-block-user", methods=["POST"])
def remove_block_user():
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        stub = get_user_grpc_stub()
        response = stub.RemoveAndBlockUser(user_pb2.UserRequest(user_id=user_id))
        return jsonify({"message": response.message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Route: Add, modify, or remove a category
@app.route("/api/manage-category", methods=["POST"])
def manage_category():
    try:
        action = request.json.get("action")
        old_category_name = request.json.get("old_category_name", "")
        new_category_name = request.json.get("new_category_name", "")
        print(action, old_category_name, new_category_name)
        if action not in ["modify", "remove"]:
            return jsonify({"error": "Invalid action"}), 400
        
        # Get all items of this category
        get_by_category_url = "http://127.0.0.1:9090/items/category/" + old_category_name
        response = requests.get(get_by_category_url)
        modified_count = len(response.json())

        if action == "modify":
            update_category = new_category_name
        else:
            update_category = None

        # query = {"category": update_category}
        update_url = "http://127.0.0.1:9090/items/"
        for item in response.json():
            item['category'] = update_category
            temp_update_url = update_url + item['_id']
            temp_rep = requests.put(temp_update_url, json=item)

        return jsonify({"message": str(modified_count) + " items' category are updated."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Route: View flagged items
@app.route("/api/flagged-items", methods=["GET"])
def flagged_items():
    item_filter_url = "http://127.0.0.1:9090/items/filter"
    try:
        query = {"flagged": True}
        # json_query = json.dumps(query)
        response = requests.post(item_filter_url, json=query)
        return jsonify({"flagged_items": response.json()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Route: View active auctions
@app.route("/api/active-auctions", methods=["GET"])
def active_auctions():
    try:
        query = {"active": True}
        json_query = json.dumps(query)
        stub = get_grpc_stub()
        response = stub.GetAuctions(service_pb2.GetAuctionRequest(query=json_query))
        # print(type(response.auctions))

        active_auction_list = []
        for auction in response.auctions:
            print(auction._id)
            temp_dict = auction_to_dict(auction)
            active_auction_list.append(temp_dict)

        return jsonify({"active_auctions": active_auction_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Route: Examine metrics
@app.route("/api/metrics", methods=["GET"])
def metrics():
    try:
        # Get query parameters
        days = int(request.args.get("days", 0))
        weeks = int(request.args.get("weeks", 0))
        months = int(request.args.get("months", 0))

        timeframe_days = days + (weeks * 7) + (months * 30)

        # Query MongoDB for auctions closed in the calculated timeframe
        start_date = datetime.isoformat(datetime.utcnow() - timedelta(days=timeframe_days))
        # print(datetime.isoformat(start_date))
        query = {"active": False, "ending_time": {"$gte": start_date}}
        json_query = json.dumps(query)
        # Pass the values to the gRPC stub
        stub = get_grpc_stub()
        response = stub.GetAuctions(
            service_pb2.GetAuctionRequest(query=json_query)
        )

        active_auction_list = []
        for auction in response.auctions:
            temp_dict = auction_to_dict(auction)
            active_auction_list.append(temp_dict)

        return jsonify({"active_auctions": active_auction_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Route: Respond to emails
@app.route("/api/respond-email", methods=["POST"])
def respond_email():
    try:
        email_id = request.json.get("email_id")
        response_text = request.json.get("response_text")

        if not email_id or not response_text:
            return jsonify({"error": "email_id and response_text are required"}), 400

        stub = get_grpc_stub()
        response = stub.RespondToEmails(admin_service_pb2.EmailRequest(email_id=email_id, response_text=response_text))
        return jsonify({"message": response.message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/unresponded-emails", methods=["GET"])
def unresponded_emails():
    try:
        # Call gRPC service
        stub = get_grpc_stub()
        response = stub.ViewUnrespondedEmails(admin_service_pb2.Empty())

        # Convert response to JSON format
        emails = [
            {
                "email_id": email.email_id,
                "user_email": email.user_email,
                "message": email.message,
            }
            for email in response.emails
        ]
        return jsonify({"unresponded_emails": emails})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
