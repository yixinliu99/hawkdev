import abc

from Auction.dao.mongoDAO import MongoDao


class Model(abc.ABC):
    def __init__(self, model_id: int):
        self.id = model_id

    def to_dict(self):
        raise NotImplementedError

    @staticmethod
    def from_dict(data):
        raise NotImplementedError

    def create(self, dao: MongoDao):
        raise NotImplementedError

    @staticmethod
    def filter(query: dict, dao: MongoDao):
        raise NotImplementedError

    def update(self, dao: MongoDao):
        raise NotImplementedError

    def delete(self, dao: MongoDao):
        raise NotImplementedError


class Bid:
    def __init__(self, bid_id, auction_id, bidder_id, bid_price):
        self.bid_id = bid_id
        self.auction_id = auction_id
        self.bidder_id = bidder_id
        self.bid_price = bid_price

    def to_dict(self):
        return {"bid_id": self.bid_id, "auction_id": self.auction_id, "bidder_id": self.bidder_id,
                "bid_price": self.bid_price}

    @staticmethod
    def from_dict(bid_dict):
        return Bid(bid_id=bid_dict["bid_id"], auction_id=bid_dict["auction_id"], bidder_id=bid_dict["bidder_id"],
                   bid_price=bid_dict["bid_price"])


