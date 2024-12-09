import os
import requests

class ItemConnector:
    def __init__(self):
        if not os.getenv("ITEM_SERVICE_ADDRESS"):
            raise ValueError("ITEM_SERVICE_ADDRESS environment variable not set")
        self.item_service_address = os.getenv("ITEM_SERVICE_ADDRESS")

    def get_item(self, item_id):
        response = requests.get(f"{self.item_service_address}/item/{item_id}")
        return response.json()

    def get_items(self):
        response = requests.get(f"{self.item_service_address}/items")
        return response.json()

    def add_item(self, item):
        response = requests.post(f"{self.item_service_address}/item", json=item)
        return response.json()

    def update_item(self, item_id, item):
        response = requests.put(f"{self.item_service_address}/item/{item_id}", json=item)
        return response.json()

    def delete_item(self, item_id):
        response = requests.delete(f"{self.item_service_address}/item/{item_id}")
        return response.json()

    def get_item_bids(self, item_id):
        response = requests.get(f"{self.item_service_address}/item/{item_id}/bids")
        return response.json()

    def add_bid_to_item(self, item_id, bid):
        response = requests.post(f"{self.item_service_address}/item/{item_id}/bid", json=bid)
        return response.json()