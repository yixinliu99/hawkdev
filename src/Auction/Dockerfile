FROM python:3.12-slim

ARG AUCTION_FOLDER=/Auction

COPY . $AUCTION_FOLDER

RUN apt update && \
  apt install -y --no-install-recommends gcc python3-dev libssl-dev rabbitmq-server && \
  apt remove -y gcc python3-dev libssl-dev && \
  apt autoremove -y
RUN pip install --no-cache-dir -r AUCTION_FOLDER/requirements.txt

ENV AUCTION_SERVICE_RABBITMQ_PORT=12345
ENV AUCTION_SERVICE_PORT=23456

WORKDIR /

RUN chmod +x AUCTION_FOLDER/serve.sh

ENTRYPOINT $AUCTION_FOLDER/serve.sh
