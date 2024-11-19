from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBManager:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="test_db"):
        """
        Initialize the MongoDBManager with the connection URI and database name.
        """
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            print(f"Connected to MongoDB database: {db_name}")
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise

    def write_to_db(self, collection_name, data):
        """
        Insert a single document or multiple documents into a collection.
        """
        collection = self.db[collection_name]
        if isinstance(data, list):
            result = collection.insert_many(data)
            print(f"Inserted {len(result.inserted_ids)} documents into {collection_name}.")
            return result.inserted_ids
        else:
            result = collection.insert_one(data)
            print(f"Inserted document with ID: {result.inserted_id} into {collection_name}.")
            return result.inserted_id

    def read_from_db(self, collection_name, query={}, projection=None):
        """
        Retrieve documents from a collection based on a query.
        """
        collection = self.db[collection_name]
        results = collection.find(query, projection)
        return list(results)

    def update_db(self, collection_name, query, update, many=False):
        """
        Update documents in a collection based on a query.
        """
        collection = self.db[collection_name]
        if many:
            result = collection.update_many(query, update)
            print(f"Updated {result.modified_count} documents in {collection_name}.")
        else:
            result = collection.update_one(query, update)
            print(f"Updated {result.modified_count} document in {collection_name}.")
        return result.modified_count

    def delete_from_db(self, collection_name, query, many=False):
        """
        Delete documents from a collection based on a query.
        """
        collection = self.db[collection_name]
        if many:
            result = collection.delete_many(query)
            print(f"Deleted {result.deleted_count} documents from {collection_name}.")
        else:
            result = collection.delete_one(query)
            print(f"Deleted {result.deleted_count} document from {collection_name}.")
        return result.deleted_count

    def list_collections(self):
        """
        List all collections in the database.
        """
        return self.db.list_collection_names()

    def drop_collection(self, collection_name):
        """
        Drop a collection from the database.
        """
        self.db[collection_name].drop()
        print(f"Dropped collection: {collection_name}.")

    def close_connection(self):
        """
        Close the MongoDB connection.
        """
        self.client.close()
        print("MongoDB connection closed.")


if __name__ == "__main__":
    # Initialize the database manager
    db_manager = MongoDBManager(db_name="my_database")

    # Write data to a collection
    data = {"name": "Alice", "age": 30}
    db_manager.write_to_db("users", data)

    # Read data from the collection
    users = db_manager.read_from_db("users")
    print("Users:", users)

    # Update a document
    db_manager.update_db("users", {"name": "Alice"}, {"$set": {"age": 31}})

    # Delete a document
    db_manager.delete_from_db("users", {"name": "Alice"})

    # List collections
    print("Collections:", db_manager.list_collections())

    # Drop a collection
    db_manager.drop_collection("users")

    # Close the connection
    db_manager.close_connection()
