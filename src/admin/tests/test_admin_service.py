import pytest
from unittest.mock import MagicMock
from admin.admin_rpc.admin_service import AdminService
from admin.admin_rpc.admin_service_pb2 import Response, FlaggedItemsResponse, ActiveAuctionsResponse, MetricsResponse


@pytest.fixture
def admin_service():
    """Fixture to create an AdminService instance with a mocked DAO."""
    service = AdminService()
    service.dao = MagicMock()  # Mock the DAO
    return service


def test_stop_auction_early(admin_service):
    # Mock DAO method
    admin_service.dao.stop_auction_early.return_value.modified_count = 1

    # Call the gRPC method
    request = MagicMock(auction_id="auction123")
    response = admin_service.StopAuctionEarly(request, None)

    # Assert the result
    assert isinstance(response, Response)
    assert response.message == "Auction stopped successfully."


def test_remove_and_block_user(admin_service):
    # Mock DAO method
    admin_service.dao.block_user_and_remove_auctions.return_value = (1, 5)

    # Call the gRPC method
    request = MagicMock(user_id="user123")
    response = admin_service.RemoveAndBlockUser(request, None)

    # Assert the result
    assert isinstance(response, Response)
    assert response.message == "User blocked and 5 auctions removed."


def test_add_modify_remove_category(admin_service):
    # Mock DAO methods
    admin_service.dao.add_category.return_value = None
    admin_service.dao.modify_category.return_value.modified_count = 1
    admin_service.dao.remove_category.return_value.deleted_count = 1

    # Add category
    add_request = MagicMock(action="add", category_id="cat123", category_name="Electronics")
    add_response = admin_service.AddModifyRemoveCategory(add_request, None)
    assert add_response.message == "Category added."

    # Modify category
    modify_request = MagicMock(action="modify", category_id="cat123", category_name="Updated Electronics")
    modify_response = admin_service.AddModifyRemoveCategory(modify_request, None)
    assert modify_response.message == "Category modified."

    # Remove category
    remove_request = MagicMock(action="remove", category_id="cat123", category_name="")
    remove_response = admin_service.AddModifyRemoveCategory(remove_request, None)
    assert remove_response.message == "Category removed."


def test_view_flagged_items(admin_service):
    # Mock DAO method
    admin_service.dao.get_flagged_items.return_value = [{"_id": "item1"}, {"_id": "item2"}]

    # Call the gRPC method
    request = MagicMock()
    response = admin_service.ViewFlaggedItems(request, None)

    # Assert the result
    assert isinstance(response, FlaggedItemsResponse)
    assert response.flagged_items == ["item1", "item2"]


def test_view_active_auctions(admin_service):
    # Mock DAO method
    admin_service.dao.get_active_auctions.return_value = [{"_id": "auction1"}, {"_id": "auction2"}]

    # Call the gRPC method
    request = MagicMock(sort_by="end_time")
    response = admin_service.ViewActiveAuctions(request, None)

    # Assert the result
    assert isinstance(response, ActiveAuctionsResponse)
    assert response.active_auctions == ["auction1", "auction2"]


def test_examine_metrics(admin_service):
    # Mock DAO method
    admin_service.dao.get_closed_auctions_count.return_value = 10

    # Call the gRPC method
    request = MagicMock(timeframe="day")
    response = admin_service.ExamineMetrics(request, None)

    # Assert the result
    assert isinstance(response, MetricsResponse)
    assert response.metrics == {"closed_auctions": 10}
