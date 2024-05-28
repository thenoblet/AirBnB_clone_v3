#!/usr/bin/python3

""" API endpoints handler module """

from api.v1.views import app_views
from flask import jsonify
from models.storage import count


@app_views.route("/status")
def get_status():
    """Returns the status of the API service."""
    data = {"status": "OK"}
    return jsonify(data)

@app_views.route("/stats")
def get_stats():
    return jsonify(
        {
            "amenities": count('Amenity'),
            "cities": count('City'),
            "places": count('Place'),
            "reviews": count('Review'),
            "states": count('State'),
            "users": count('User')
        }
    )
