from Item.models.item import Item
from Item.consts.consts import MONGO_TEST_DB
from Item.dao.mongoDAO import MongoDao

import pymongo

new_item = Item(
    user_id="zxcv",
    starting_price=100,
    quantity=1,
    shipping_cost=1,
    description="First item",
    category="clothes",
    flagged=True
)

dao = MongoDao()

new_item.create(dao)