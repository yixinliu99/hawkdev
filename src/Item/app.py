import logging
import os

from flask import Flask, request
from flask_cors import CORS

from Item.dao.mongoDAO import MongoDao
from Item.views import item_api

LOG_FILE = "flask_app_exceptions.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)
CORS(app)

app.dao = MongoDao()
app.register_blueprint(item_api)


@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(
        f"Exception occurred during {request.method} {request.url}: {e}",
        exc_info=True
    )
    return {"error": "Internal Server Error"}, 500


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_SERVER_PORT", 9090))
    logging.info(f"Starting Flask server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
