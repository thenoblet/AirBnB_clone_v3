#!/usr/bin/python3
""" App routing module for all APIs in the Flask app """

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_session(self):
    """
    Remove the current SQLAlchemy Session after each request.

    Args:
    self: The Flash application context.
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    Handles 404 errors for page not found.

    Args:
    error: The error object.

    Returns:
    A JSON response with the error message and status code 404.
    """
    data = {"error": "Not found"}
    return jsonify(data), 404


if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=int(os.getenv("HBNB_API_PORT", default="5000")),
            threaded=True
    )
