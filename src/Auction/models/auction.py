import datetime

from Auction.consts.consts import AUCTIONS_COLLECTION
from Auction.dao.mongoDAO import MongoDao
from Auction.models.models import Model, Bid
from bson import ObjectId


class Auction(Model):
    def __init__(self, item_id, seller_id, starting_time: str, ending_time: str,
                 starting_price: float, current_price: float, active: bool = False,
                 bids: list[Bid] = None, auction_id=None):
        super().__init__(auction_id)
        self.item_id = item_id
        self.seller_id = seller_id
        self.active = active
        self.starting_time = datetime.datetime.fromisoformat(starting_time)
        self.ending_time = datetime.datetime.fromisoformat(ending_time)
        self.starting_price = starting_price
        self.current_price = current_price
        self.bids = bids

    def to_dict(self):
        return {"item_id": self.item_id, "seller_id": self.seller_id, "active": self.active,
                "starting_time": datetime.datetime.isoformat(self.starting_time), "ending_time": datetime.datetime.isoformat(self.ending_time),
                "starting_price": self.starting_price, "current_price": self.current_price, "bids": self.bids}

    @staticmethod
    def from_dict(auction_dict: dict):
        return Auction(item_id=auction_dict["item_id"], seller_id=auction_dict["seller_id"], active=auction_dict["active"],
                       starting_time=auction_dict["starting_time"], ending_time=auction_dict["ending_time"],
                       starting_price=auction_dict["starting_price"], current_price=auction_dict["current_price"],
                       bids=auction_dict["bids"], auction_id=auction_dict["id"])

    def create(self, dao: MongoDao) -> list[str] :
        return dao.write_to_db(AUCTIONS_COLLECTION, self.to_dict())

    def update(self, dao: MongoDao) -> int :
        return dao.update_db(AUCTIONS_COLLECTION, {"id": self.id}, self.to_dict())

    @staticmethod
    def filter(query: dict, dao: MongoDao) -> list:
        return dao.read_from_db(AUCTIONS_COLLECTION, query)

    def delete(self, dao: MongoDao):
        return dao.delete_from_db(AUCTIONS_COLLECTION, {"id": self.id})

    def start_auction(self, dao: MongoDao):
        # validate auction
        valid, msg = self._validate_auction()
        if not valid:
            raise Exception(msg)

        # update auction status
        return dao.update_db(AUCTIONS_COLLECTION, {"id": self.id}, {"active": True})

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
