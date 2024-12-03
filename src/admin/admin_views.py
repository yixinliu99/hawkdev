from flask import Flask, request, jsonify, render_template
import grpc
import grpc.admin_service_pb2 as admin_service_pb2
import grpc.admin_service_pb2_grpc as admin_service_pb2_grpc

app = Flask(__name__)

# gRPC connection setup
def get_grpc_stub():
    channel = grpc.insecure_channel("localhost:50051")  # Connect to the gRPC server
    return admin_service_pb2_grpc.AdminServiceStub(channel)


# API Route: Stop an auction early
@app.route("/api/stop-auction", methods=["POST"])
def stop_auction():
    try:
        auction_id = request.json.get("auction_id")
        if not auction_id:
            return jsonify({"error": "auction_id is required"}), 400

        stub = get_grpc_stub()
        response = stub.StopAuctionEarly(admin_service_pb2.AuctionRequest(auction_id=auction_id))
        return jsonify({"message": response.message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Route: Remove and block a user
@app.route("/api/remove-block-user", methods=["POST"])
def remove_block_user():
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        stub = get_grpc_stub()
        response = stub.RemoveAndBlockUser(admin_service_pb2.UserRequest(user_id=user_id))
        return jsonify({"message": response.message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Route: Add, modify, or remove a category
@app.route("/api/manage-category", methods=["POST"])
def manage_category():
    try:
        action = request.json.get("action")
        category_id = request.json.get("category_id")
        category_name = request.json.get("category_name", "")

        if action not in ["add", "modify", "remove"]:
            return jsonify({"error": "Invalid action"}), 400
        if not category_id:
            return jsonify({"error": "category_id is required"}), 400

        stub = get_grpc_stub()
        response = stub.AddModifyRemoveCategory(
            admin_service_pb2.CategoryRequest(action=action, category_id=category_id, category_name=category_name)
        )
        return jsonify({"message": response.message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Route: View flagged items
@app.route("/api/flagged-items", methods=["GET"])
def flagged_items():
    try:
        stub = get_grpc_stub()
        response = stub.ViewFlaggedItems(admin_service_pb2.Empty())
        return jsonify({"flagged_items": response.flagged_items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Route: View active auctions
@app.route("/api/active-auctions", methods=["GET"])
def active_auctions():
    try:
        sort_by = request.args.get("sort_by", "end_time")

        stub = get_grpc_stub()
        response = stub.ViewActiveAuctions(admin_service_pb2.SortingRequest(sort_by=sort_by))
        return jsonify({"active_auctions": response.active_auctions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Route: Examine metrics
@app.route("/api/metrics", methods=["GET"])
def metrics():
    try:
        timeframe = request.args.get("timeframe", "day")

        stub = get_grpc_stub()
        response = stub.ExamineMetrics(admin_service_pb2.MetricsRequest(timeframe=timeframe))
        return jsonify({"metrics": dict(response.metrics)})
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


# # Frontend Route: Admin Dashboard
# @app.route("/")
# def dashboard():
#     return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
