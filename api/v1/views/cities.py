#!/usr/bin/python3
"""
This module provides RESTful API views for managing City
objects related to State objects.

The views include:
- Retrieving cities by state ID
- Retrieving a city by ID
- Deleting a city by ID
- Creating a new city in a state
- Updating an existing city

The routes are registered with Flask's `app_views` blueprint.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities_by_state(state_id):
    """
    Retrieve all cities in a specified state.

    Args:
        state_id (str): The ID of the state.

    Returns:
        Response: A JSON response containing a list of cities
        in the state, or a 404 error if the state is not found.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city_by_id(city_id):
    """
    Retrieve a city by its ID.

    Args:
        city_id (str): The ID of the city.

    Returns:
        Response: A JSON response containing the city's details,
                  or a 404 error if the city is not found.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city_by_id(city_id):
    """
    Delete a city by its ID.

    Args:
        city_id (str): The ID of the city to delete.

    Returns:
        Response: A JSON response with an empty dictionary and a
        200 status code, or a 404 error if the city is not found.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """
    Create a new city in a specified state.

    Args:
        state_id (str): The ID of the state to create the city in.

    Returns:
        Response: A JSON response containing the details of the
        newly created city with a 201 status code, or an error
        response if the input data is invalid or the state
        is not found.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json(force=True, silent=True, cache=False)
    if not data:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    new_city = City(state_id=state.id, **data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """
    Update an existing city by its ID.

    Args:
        city_id (str): The ID of the city to update.

    Returns:
        Response: A JSON response containing the updated
        city's details, or an error response if the input data
        is invalid or the city is not found.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json(force=True, silent=True, cache=False)
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
