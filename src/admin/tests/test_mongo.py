import mongomock
import pytest
from admin.dao.mongoDAO import MongoDAO


@pytest.fixture
def mongo_dao():
    """Fixture to create a MongoDAO instance with a mocked MongoDB client using mongomock."""
    mock_client = mongomock.MongoClient()
    return MongoDAO(client=mock_client)  # Pass the mocked client to the DAO


def test_stop_auction_early(mongo_dao):
    # Insert a mock auction
    mongo_dao.db.auctions.insert_one({"_id": "auction123", "status": "active"})

    # Call the method
    result = mongo_dao.stop_auction_early("auction123")

    # Assert the result
    assert result.modified_count == 1
    auction = mongo_dao.db.auctions.find_one({"_id": "auction123"})
    assert auction["status"] == "stopped"


def test_block_user_and_remove_auctions(mongo_dao):
    # Insert a mock user and auctions
    mongo_dao.db.users.insert_one({"_id": "user123", "blocked": False})
    mongo_dao.db.auctions.insert_many([
        {"_id": "auction1", "user_id": "user123"},
        {"_id": "auction2", "user_id": "user123"},
    ])

    # Call the method
    user_result, auction_result = mongo_dao.block_user_and_remove_auctions("user123")

    # Assert the results
    assert user_result == 1
    assert auction_result == 2
    user = mongo_dao.db.users.find_one({"_id": "user123"})
    assert user["blocked"] is True


def test_add_category(mongo_dao):
    # Call the method
    mongo_dao.add_category("cat123", "Electronics")

    # Assert the result
    category = mongo_dao.db.categories.find_one({"_id": "cat123"})
    assert category["name"] == "Electronics"


def test_modify_category(mongo_dao):
    # Insert a mock category
    mongo_dao.db.categories.insert_one({"_id": "cat123", "name": "Old Electronics"})

    # Call the method
    result = mongo_dao.modify_category("cat123", "Updated Electronics")

    # Assert the result
    assert result.modified_count == 1
    category = mongo_dao.db.categories.find_one({"_id": "cat123"})
    assert category["name"] == "Updated Electronics"


def test_remove_category(mongo_dao):
    # Insert a mock category
    mongo_dao.db.categories.insert_one({"_id": "cat123", "name": "Electronics"})

    # Call the method
    result = mongo_dao.remove_category("cat123")

    # Assert the result
    assert result.deleted_count == 1
    category = mongo_dao.db.categories.find_one({"_id": "cat123"})
    assert category is None


def test_get_flagged_items(mongo_dao):
    # Insert mock flagged items
    mongo_dao.db.items.insert_many([
        {"_id": "item1", "flagged": True},
        {"_id": "item2", "flagged": True},
        {"_id": "item3", "flagged": False},
    ])

    # Call the method
    result = list(mongo_dao.get_flagged_items())

    # Assert the result
    assert len(result) == 2
    assert {"_id": "item1", "flagged": True} in result
    assert {"_id": "item2", "flagged": True} in result


def test_get_active_auctions(mongo_dao):
    # Insert mock active auctions
    mongo_dao.db.auctions.insert_many([
        {"_id": "auction1", "status": "active", "end_time": 1},
        {"_id": "auction2", "status": "active", "end_time": 2},
        {"_id": "auction3", "status": "closed", "end_time": 3},
    ])

    # Call the method
    result = list(mongo_dao.get_active_auctions("end_time"))

    # Assert the result
    assert len(result) == 2
    assert result[0]["_id"] == "auction1"  # Sorted by end_time


def test_get_closed_auctions_count(mongo_dao):
    # Insert mock closed auctions
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    mongo_dao.db.auctions.insert_many([
        {"_id": "auction1", "status": "closed", "end_time": now - timedelta(days=1)},
        {"_id": "auction2", "status": "closed", "end_time": now - timedelta(days=7)},
        {"_id": "auction3", "status": "active", "end_time": now - timedelta(days=1)},
    ])

    # Call the method
    result = mongo_dao.get_closed_auctions_count("day")

    # Assert the result
    assert result == 1  # Only one closed auction in the last day
