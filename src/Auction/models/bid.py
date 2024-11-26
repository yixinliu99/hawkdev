from Auction.consts.consts import BIDS_COLLECTION

class Bid:
    def __init__(self, auction_id, user_id, bid_amount):
        self.auction_id = auction_id
        self.user_id = user_id
        self.bid_amount = bid_amount

    def to_dict(self):
        return {"auction_id": self.auction_id, "user_id": self.user_id,
                "bid_amount": self.bid_amount}

    @staticmethod
    def from_dict(bid_dict):
        return Bid(auction_id=bid_dict["auction_id"], user_id=bid_dict["user_id"],
                   bid_amount=bid_dict["bid_amount"])

    def create(self, dao):
        return dao.write_to_db(BIDS_COLLECTION, self.to_dict())
