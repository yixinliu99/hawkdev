from flask import Flask
from .config import Config
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mongo = PyMongo(app)
    return app
