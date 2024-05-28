#!/usr/bin/python3

""" API endpoints handler module """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def get_status():
    """Returns the status of the API service."""
    data = {"status": "OK"}
    return jsonify(data)


@app_views.route("/stats")
def get_stats():
    """Returns statistics about the API service."""
    return jsonify(
        {
            "amenities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')
        }
    )
