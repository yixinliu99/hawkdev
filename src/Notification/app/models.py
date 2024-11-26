from flask_pymongo import PyMongo
mongo = PyMongo()

class Notification:
    def __init__(self, user_id, message, timestamp):
        self.user_id = user_id
        self.message = message
        self.timestamp = timestamp
