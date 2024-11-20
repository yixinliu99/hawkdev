from flask import app
from src.Auction.db.mongoDbManager import MongoDBManager

app = app.Flask(__name__)
app.mdb = MongoDBManager()

if __name__ == "__main__":
    app.run(debug=True)
