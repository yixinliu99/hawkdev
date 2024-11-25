from typing import Any, Callable

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import Auction.consts.apiKeys as apiKeys  # Should not be committed to the repo
import Auction.consts.consts as consts

def ensure_connection(func: Callable) -> Callable:
    def wrapper(self, *args, **kwargs):
        self._check_connection()
        return func(self, *args, **kwargs)
    return wrapper


class MongoDao:
    def __init__(self, db_name: str=consts.MONGO_TEST_DB, uri: str=apiKeys.MONGODB_URI):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None
        try:
            self._connect_to_db()
        except ConnectionFailure as e:
            raise

    def _connect_to_db(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
        except ConnectionFailure as e:
            raise

    def _check_connection(self):
        try:
            self.client.admin.command('ping')
        except ConnectionFailure:
            self._connect_to_db()

    @ensure_connection
    def write_to_db(self, collection_name: str, data: Any) -> Any:
        collection = self.db[collection_name]
        if isinstance(data, list):
            result = collection.insert_many(data)
            print(f"Inserted {len(result.inserted_ids)} documents into {collection_name}.")
            return result.inserted_ids
        else:
            result = collection.insert_one(data)
            print(f"Inserted document with ID: {result.inserted_id} into {collection_name}.")
            return result.inserted_id

    @ensure_connection
    def read_from_db(self, collection_name, query: dict, projection=None) -> list:
        """
        Retrieve documents based on query ignoring hidden documents.
        """
        collection = self.db[collection_name]
        query = {**query, "hidden": {"$ne": True}}
        results = collection.find(query, projection)
        return list(results)

    @ensure_connection
    def update_db(self, collection_name, query: dict, update: Any, many=False) -> int:
        """
        Replace filtered documents with update.
        """
        collection = self.db[collection_name]
        if many:
            result = collection.update_many(query, update)
        else:
            result = collection.update_one(query, update)
        return result.modified_count

    @ensure_connection
    def delete_from_db(self, collection_name: str, query: dict, many=False) -> int:
        """
        Hide (not actually delete) documents from a collection based on a query.
        """
        collection = self.db[collection_name]
        if many:
            result = collection.update_many(query, {"$set": {"hidden": True}})
        else:
            result = collection.update_one(query, {"$set": {"hidden": True}})
        return result.modified_count

    def close_connection(self):
        try:
            self.client.close()
        except ConnectionFailure:
            pass
