#!/usr/bin/python3
""" AirBnB clone - RESTful API """
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(e):
    """ close the storage """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ handler for 404 errors """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST")
    port = int(os.getenv("HBNB_API_PORT"))

    if not host or not port:
        host = "0.0.0.0"
        port = 5000

    app.run(host=host, port=port, threaded=True)
