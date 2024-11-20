import abc
from src.Auction.consts.consts import AUCTIONS_COLLECTION

class Model(abc.ABC):
    def __init__(self, model_id):
        self.id = model_id

    def to_dict(self):
        raise NotImplementedError

    @staticmethod
    def from_dict(data):
        raise NotImplementedError

    def save_to_db(self):
        raise NotImplementedError

    @staticmethod
    def read_from_db(query):
        raise NotImplementedError

    def update_db(self, update):
        raise NotImplementedError

    def delete_from_db(self):
        raise NotImplementedError


class Auction(Model):
    def __init__(self, item_id, seller_id, starting_time, ending_time, starting_price, current_price, bids, auction_id=None):
        super().__init__(auction_id)
        self.item_id = item_id
        self.seller_id = seller_id
        self.starting_time = starting_time
        self.ending_time = ending_time
        self.starting_price = starting_price
        self.current_price = current_price
        self.bids = bids

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "seller_id": self.seller_id,
            "start_time": self.starting_time,
            "ending_time": self.ending_time,
            "starting_price": self.starting_price,
            "current_price": self.current_price,
            "bids": self.bids
        }

    @staticmethod
    def from_dict(auction_dict):
        return Auction(
            item_id=auction_dict["item_id"],
            seller_id=auction_dict["seller_id"],
            starting_time=auction_dict["starting_time"],
            ending_time=auction_dict["ending_time"],
            starting_price=auction_dict["starting_price"],
            current_price=auction_dict["current_price"],
            bids=auction_dict["bids"],
            auction_id=auction_dict["id"]
        )

    def save_to_db(self):
        return app.mdb.write_to_db(collection_name=AUCTIONS_COLLECTION, data=self.to_dict())

    @staticmethod
    def read_from_db(query):
        return app.mdb.read_from_db(AUCTIONS_COLLECTION, query)

    def update_db(self, update):
        return app.mdb.update_db(AUCTIONS_COLLECTION, {"id": self.id}, update)

    def delete_from_db(self):
        return app.mdb.delete_from_db(AUCTIONS_COLLECTION, {"id": self.id})


class Bid:
    def __init__(self, bid_id, auction_id, bidder_id, bid_price):
        self.bid_id = bid_id
        self.auction_id = auction_id
        self.bidder_id = bidder_id
        self.bid_price = bid_price

    def to_dict(self):
        return {
            "bid_id": self.bid_id,
            "auction_id": self.auction_id,
            "bidder_id": self.bidder_id,
            "bid_price": self.bid_price
        }

    @staticmethod
    def from_dict(bid_dict):
        return Bid(
            bid_id=bid_dict["bid_id"],
            auction_id=bid_dict["auction_id"],
            bidder_id=bid_dict["bidder_id"],
            bid_price=bid_dict["bid_price"]
        )

