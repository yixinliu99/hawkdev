from flask import Flask, request, jsonify
from werkzeug.exceptions import NotFound, BadRequest
from flask import Blueprint
from connectors.auction.auction_rpc_client import filter_auctions, create_auction, place_bid,buy_now
auction_api = Blueprint("auction", __name__)

@auction_api.route("/auctions/<auction_id>", methods=["GET"])
def get_auction_by_id(auction_id):
    response = filter_auctions({"_id": auction_id})

    if not response['success']:
        raise NotFound(response['message'])

    return jsonify(response['auctions'][0])


@auction_api.route("/auctions/create", methods=["POST"])
def create_auction_api():
    data = request.json
    response = create_auction(
        float(data["starting_price"]),
        data["starting_time"],
        data["ending_time"],
        data["seller_id"],
        data["item_id"],
        float(data["buy_now_price"])
    )

    return jsonify(response)


@auction_api.route("/auctions/place_bid", methods=["POST"])
def place_bid_api():
    data = request.json
    response = place_bid(data["auction_id"], data["user_id"], float(data["bid_amount"]))

    return jsonify(response)

@auction_api.route("/auctions/buy_now/<auction_id>", methods=["POST"])
def buy_now_api(auction_id):
    data = request.json
    response = buy_now(auction_id, data["user_id"])

    return jsonify(response)
