#!/usr/bin/python3

""" App routing module """

import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_session(self):
    """
    Remove the current SQLAlchemy Session after each request.

    This function is registered to be called after each request to ensure
    that the SQLAlchemy Session is properly closed,
    preventing any potential resource leaks.
    """
    storage.close()


if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=int(os.getenv("HBNB_API_PORT", default="5000")),
            threaded=True
    )
