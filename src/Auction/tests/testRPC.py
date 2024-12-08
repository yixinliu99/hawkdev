import datetime
from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from bson import ObjectId

from Auction.rpc import service_pb2, service_pb2_grpc
from Auction.rpc.service import AuctionService


@pytest.fixture(scope='module')
def mock_dao():
    dao = MagicMock()

    return dao


@pytest.fixture(scope='module')
def auction_service(mock_dao):
    return AuctionService(mock_dao)


@pytest.fixture(scope='module')
def grpc_add_to_server():
    return service_pb2_grpc.add_AuctionServiceServicer_to_server


@pytest.fixture(scope='module')
def grpc_servicer(auction_service):
    return auction_service


@pytest.fixture(scope='module')
def grpc_stub_cls():
    return service_pb2_grpc.AuctionServiceStub


@patch('Auction.task_scheduler.tasks.start_auction_task.apply_async', MagicMock())
def test_create_auction_success(grpc_stub, mock_dao):
    mock_dao.write_to_db.return_value = ["wakemeupwhenseptemberends"]

    request = service_pb2.CreateAuctionRequest(
        starting_price=100.00,
        starting_time=(datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(seconds=10)).isoformat(),
        ending_time=(datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(seconds=20)).isoformat(),
        item_id="1",
        seller_id="asd",
    )

    response = grpc_stub.CreateAuction(request)
    assert response.success
    assert response.auction_id == "wakemeupwhenseptemberends"


def test_create_auction_failure(grpc_stub, mock_dao):
    mock_dao.write_to_db.side_effect = Exception()

    request = service_pb2.CreateAuctionRequest(
        starting_price=100.00,
        starting_time=(datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(seconds=10)).isoformat(),
        ending_time=(datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(seconds=20)).isoformat(),
        item_id="1",
        seller_id="asd",
    )

    response = grpc_stub.CreateAuction(request)
    assert not response.success


@patch('Auction.task_scheduler.tasks.start_auction_task.AsyncResult', MagicMock())
@patch('Auction.task_scheduler.tasks.start_auction_task.apply_async', MagicMock())
def test_update_auction_success(grpc_stub, mock_dao):
    fake_id = str(ObjectId())
    mock_dao.read_from_db.return_value = [{
        "_id": fake_id,
        "starting_price": 100.00,
        "starting_time": "2024-11-25T10:30:00",
        "ending_time": "2024-11-25T12:30:00",
        "seller_id": "2",
        "item_id": "1",
        "current_price": 100.00,
        "bids": []
    }]
    mock_dao.update.return_value = 1

    request = service_pb2.UpdateAuctionRequest(
        auction_id=fake_id,
        starting_price=120.00,
        starting_time="2024-11-25T10:30:00",
        ending_time="2024-11-25T12:30:00",
        seller_id="2",
        item_id="1"
    )

    response = grpc_stub.UpdateAuction(request)
    assert response.success


def test_start_auction_success(grpc_stub, mock_dao):
    fake_id = str(ObjectId())
    mock_dao.read_from_db.return_value = [{
        "_id": fake_id,
        "starting_price": 100.00,
        "starting_time": (datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(seconds=10)).isoformat(),
        "ending_time": (datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(seconds=20)).isoformat(),
        "seller_id": 2,
        "item_id": 1,
        "active": False,
        "current_price": 100.00,
        "bids": []
    }]
    mock_dao.update.return_value = 1

    request = service_pb2.StartAuctionRequest(auction_id=fake_id)

    response = grpc_stub.StartAuction(request)
    assert response.success


def test_stop_auction_success(grpc_stub, mock_dao):
    fake_id = str(ObjectId())
    mock_dao.read_from_db.return_value = [{
        "_id": fake_id,
        "starting_price": 100.00,
        "starting_time": (datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(seconds=10)).isoformat(),
        "ending_time": (datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(seconds=20)).isoformat(),
        "seller_id": 2,
        "item_id": 1,
        "active": True,
        "current_price": 100.00,
        "bids": []
    }]
    mock_dao.update.return_value = 1

    request = service_pb2.StopAuctionRequest(auction_id=fake_id)

    response = grpc_stub.StopAuction(request)
    assert response.success


def test_place_bid_success(grpc_stub, mock_dao):
    fake_id = str(ObjectId())
    mock_dao.read_from_db.return_value = [{
        "_id": fake_id,
        "starting_price": 100.00,
        "starting_time": (datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(seconds=10)).isoformat(),
        "ending_time": (datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(seconds=20)).isoformat(),
        "seller_id": 2,
        "item_id": 1,
        "active": True,
        "current_price": 100.00,
        "bids": []
    }]
    mock_dao.update.return_value = 1

    request = service_pb2.PlaceBidRequest(
        auction_id=fake_id,
        user_id="1",
        bid_amount=120.00
    )

    response = grpc_stub.PlaceBid(request)
    assert response.success
