from flask import Flask
from Item.dao.mongoDAO import MongoDao
from Item.views import item_api
import os
app = Flask(__name__)
app.dao = MongoDao()
app.register_blueprint(item_api)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
