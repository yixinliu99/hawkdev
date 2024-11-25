import abc
import datetime

import Auction.dao.mongoDAO
from Auction.dao.mongoDAO import MongoDao
from Auction.consts.consts import AUCTIONS_COLLECTION

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


class Auction(Model):
    def __init__(self, item_id: int, seller_id: int, starting_time: datetime.datetime, ending_time: datetime.datetime,
                 starting_price: float, current_price: float, active: bool = False,
                 bids: list[Bid] = None, auction_id=None):
        super().__init__(auction_id)
        self.item_id = item_id
        self.seller_id = seller_id
        self.active = active
        self.starting_time = starting_time
        self.ending_time = ending_time
        self.starting_price = starting_price
        self.current_price = current_price
        self.bids = bids

    def to_dict(self):
        return {"item_id": self.item_id, "seller_id": self.seller_id, "active": self.active,
                "start_time": self.starting_time, "ending_time": self.ending_time,
                "starting_price": self.starting_price, "current_price": self.current_price, "bids": self.bids}

    @staticmethod
    def from_dict(auction_dict: dict):
        return Auction(item_id=auction_dict["item_id"], seller_id=auction_dict["seller_id"], active=auction_dict["active"],
                       starting_time=auction_dict["starting_time"], ending_time=auction_dict["ending_time"],
                       starting_price=auction_dict["starting_price"], current_price=auction_dict["current_price"],
                       bids=auction_dict["bids"], auction_id=auction_dict["id"])

    def create(self, dao: MongoDao):
        dao.write_to_db(AUCTIONS_COLLECTION, self.to_dict())

    def update(self, dao: MongoDao):
        dao.update_db(AUCTIONS_COLLECTION, {"id": self.id}, self.to_dict())

    @staticmethod
    def filter(query: dict, dao: MongoDao):
        return dao.read_from_db(AUCTIONS_COLLECTION, query)

    def delete(self, dao: MongoDao):
        dao.delete_from_db(AUCTIONS_COLLECTION, {"id": self.id})

    def start_auction(self, dao: MongoDao):
        # validate auction
        valid, msg = self._validate_auction()
        if not valid:
            raise Exception(msg)

        # update auction status
        dao.update_db(AUCTIONS_COLLECTION, {"id": self.id}, {"active": True})

    def _validate_auction(self) -> (bool, str):
        if self.starting_time > self.ending_time:
            return False, "Ending time must be after starting time"
        if self.starting_price < 0:
            return False, "Starting price must be positive"
        if self.current_price < 0:
            return False, "Current price must be positive"
        if self.starting_time < self.ending_time:
            return False, "Ending time must be after starting time"
        if self.starting_time <= datetime.datetime.now():
            return False, "Starting time must be in the future"

        return True, ""


