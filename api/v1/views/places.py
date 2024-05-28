#!/usr/bin/python3
'''
Routes for managing Place objects and operations.
'''
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    '''
    Retrieve the list of all Place objects of a City.

    Args:
    city_id: The ID of the City object to retrieve places for.

    Returns:
    A JSON response containing all Place objects of the specified City.
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    '''
    Retrieve a specific Place object by ID.

    Args:
    place_id: The ID of the Place object to retrieve.

    Returns:
    A JSON response containing the Place object with the specified ID,
    or 404 if the Place object was not found.
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''
    Delete a Place object by ID.

    Args:
    place_id: The ID of the Place object to delete.

    Returns:
    An empty JSON response with status code 200 if the Place was deleted
    successfully, or 404 if the Place object was not found.
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''
    Create a new Place object.

    Args:
    city_id: The ID of the City object associated with the new Place.

    Returns:
    A JSON response containing the newly created Place object.
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_data:
        abort(400, 'Missing user_id')
    if 'name' not in request_data:
        abort(400, 'Missing name')

    user = storage.get(User, request_data['user_id'])
    if user is None:
        abort(404)

    new_place = Place(city_id=city_id, **request_data)
    new_place.save()
    response = jsonify(new_place.to_dict())
    response.status_code = 201
    return response


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
    Update a specific Place object by ID.

    Args:
    place_id: The ID of the Place object to update.

    Returns:
    A JSON response containing the updated Place object on success
    (status code 200), or 404 if the Place object was not found, or
    400 if the request body is not valid JSON.
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, 'Not a JSON')

    for key, value in request_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict())
