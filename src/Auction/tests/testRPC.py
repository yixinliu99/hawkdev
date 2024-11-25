from datetime import datetime, timedelta

import pytest
from unittest.mock import MagicMock, patch
import grpc
from bson import ObjectId

from Auction.rpc import service_pb2, service_pb2_grpc
from Auction.models.auction import Auction
from Auction.rpc.service import AuctionService


@pytest.fixture(scope='module')
def mock_dao():
    dao = MagicMock()

    return dao


@pytest.fixture(scope='module')
def mock_celery():
    return MagicMock()


@pytest.fixture(scope='module')
def auction_service(mock_dao, mock_celery):
    return AuctionService(mock_dao, mock_celery)


@pytest.fixture(scope='module')
def grpc_add_to_server():
    return service_pb2_grpc.add_AuctionServiceServicer_to_server


@pytest.fixture(scope='module')
def grpc_servicer(auction_service):
    return auction_service


@pytest.fixture(scope='module')
def grpc_stub_cls():
    return service_pb2_grpc.AuctionServiceStub


def test_create_auction_success(grpc_stub, mock_dao, mock_celery):
    mock_dao.create.return_value = 1
    mock_celery.send_task.return_value = None
    mock_dao.write_to_db.return_value = ["wakemeupwhenseptemberends"]

    request = service_pb2.CreateAuctionRequest(
        starting_price="100.00",
        starting_time=(datetime.now() + timedelta(seconds=10)).isoformat(),
        ending_time=(datetime.now() + timedelta(seconds=20)).isoformat(),
        item_id=1,
        seller_id=2,
    )

    response = grpc_stub.CreateAuction(request)
    assert response.success
    assert response.auction_id == "wakemeupwhenseptemberends"
    mock_celery.send_task.assert_called_once()


def test_create_auction_failure(grpc_stub, mock_dao):
    mock_dao.create.side_effect = Exception()

    request = service_pb2.CreateAuctionRequest(
        starting_price="100.00",
        starting_time=(datetime.now() + timedelta(seconds=10)).isoformat(),
        ending_time=(datetime.now() + timedelta(seconds=20)).isoformat(),
        item_id=1,
        seller_id=2,
    )

    response = grpc_stub.CreateAuction(request)
    assert not response.success



def test_update_auction_success(grpc_stub, mock_dao):
    mock_dao.read_from_db.return_value = {
        "_id": "auction123",
        "starting_price": 100.00,
        "starting_time": "2024-11-25T10:30:00",
        "ending_time": "2024-11-25T12:30:00",
        "seller_id": 2,
        "item_id": 1,
    }
    mock_dao.update.return_value = 1

    request = service_pb2.UpdateAuctionRequest(
        auction_id=str(ObjectId()),
        starting_price="120.00",
        starting_time="2024-11-25T10:30:00",
        ending_time="2024-11-25T12:30:00",
        seller_id=2,
        item_id=1,
    )

    response = grpc_stub.UpdateAuction(request)
    assert response.success
