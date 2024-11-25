!#/bin/bash

# Generate the gRPC code
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./rpc/service.proto

# Run RabbitMQ
rabbitmq-server &

# Run service
python -m Auction.rpc.service

