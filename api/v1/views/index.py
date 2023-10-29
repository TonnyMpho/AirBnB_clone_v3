#!/usr/bin/python3
""" API blueprints """
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """ returns the status """
    return jsonify({"status": "OK"})
