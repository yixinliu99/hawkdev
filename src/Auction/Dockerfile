FROM python:3.12-slim

WORKDIR /app
COPY src/Auction/* .

RUN apt update && \
  apt install -y --no-install-recommends gcc python3-dev libssl-dev rabbitmq-server && \
  apt remove -y gcc python3-dev libssl-dev && \
  apt autoremove -y
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./rpc/service.proto

ENTRYPOINT serve.sh