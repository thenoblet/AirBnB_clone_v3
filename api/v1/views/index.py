#!/usr/bin/python3

""" API endpoints handler module """

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def get_status():
    """Returns the status of the API service."""
    data = {"status": "OK"}
    return jsonify(data)
