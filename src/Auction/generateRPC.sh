!#/bin/bash

python -m ./rpc/grpc_tools.protoc -I. --python_out=. --grpc_python_out=./rpc service.proto
