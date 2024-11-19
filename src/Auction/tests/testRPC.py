import pytest
from unittest.mock import patch
import grpc
from concurrent import futures

import service_pb2
import service_pb2_grpc


# gRPC Server Fixture
@pytest.fixture
def grpc_server():
    from microservice import MyService

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MyServiceServicer_to_server(MyService(), server)
    port = server.add_insecure_port("[::]:50052")  # Test port
    server.start()
    yield f"localhost:{port}"
    server.stop(None)


# gRPC Client Fixture
@pytest.fixture
def grpc_client(grpc_server):
    with grpc.insecure_channel(grpc_server) as channel:
        stub = service_pb2_grpc.MyServiceStub(channel)
        yield stub


# Tests for gRPC Endpoint
def test_grpc_say_hello_new_user(grpc_client, mocker):
    # Mock MongoDB
    mongo_mock = mocker.patch("microservice.greetings_collection")
    mongo_mock.find_one.return_value = None

    # Test new user
    request = service_pb2.HelloRequest(name="Alice")
    response = grpc_client.SayHello(request)
    assert response.message == "Hello, Alice!"
    mongo_mock.insert_one.assert_called_once_with(
        {"name": "Alice", "message": "Hello, Alice!"}
    )


def test_grpc_say_hello_existing_user(grpc_client, mocker):
    # Mock MongoDB
    mongo_mock = mocker.patch("microservice.greetings_collection")
    mongo_mock.find_one.return_value = {"name": "Bob", "message": "Hello, Bob!"}

    # Test existing user
    request = service_pb2.HelloRequest(name="Bob")
    response = grpc_client.SayHello(request)
    assert response.message == "Hello, Bob!"
    mongo_mock.insert_one.assert_not_called()
