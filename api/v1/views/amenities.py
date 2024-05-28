#!/usr/bin/python3
'''
Routes for managing Amenity objects and operations.
'''
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    '''
    Retrieve the list of all Amenity objects.

    Returns:
    A JSON response containing all Amenity objects.
    '''
    all_amenities = storage.all(Amenity)
    all_amenities_dict = [
            amenity.to_dict() for amenity in all_amenities.values()
    ]
    return jsonify(all_amenities_dict)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    '''
    Retrieve an Amenity object by ID.

    Args:
    amenity_id: The ID of the Amenity object to retrieve.

    Returns:
    A JSON response containing the Amenity object with the
    specified ID, or 404 if the Amenity object was not found.
    '''
    amenity_instance = storage.get(Amenity, amenity_id)
    if amenity_instance is None:
        abort(404)
    return jsonify(amenity_instance.to_dict())


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    '''
    Create a new Amenity object.

    Returns:
    A JSON response containing the newly created Amenity object.
    '''
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')

    new_amenity = Amenity(**request_data)
    new_amenity.save()
    response = jsonify(new_amenity.to_dict())
    response.status_code = 201
    return response


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''
    Update an Amenity object by ID.

    Args:
    amenity_id: The ID of the Amenity object to update.

    Returns:
    A JSON response containing the updated Amenity object on success
    (status code 200), or 404 if the Amenity object was not found, or
    400 if the request body is not valid JSON.
    '''
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, 'Not a JSON')
    amenity_instance = storage.get(Amenity, amenity_id)
    if amenity_instance is None:
        abort(404)
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_instance, key, value)
    amenity_instance.save()
    return jsonify(amenity_instance.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    '''
    Delete an Amenity object by ID.

    Args:
    amenity_id: The ID of the Amenity object to delete.

    Returns:
    An empty JSON response with status code 200 if the Amenity was deleted
    successfully, or 404 if the Amenity object was not found.
    '''
    amenity_instance = storage.get(Amenity, amenity_id)
    if amenity_instance is None:
        abort(404)
    storage.delete(amenity_instance)
    storage.save()
    return jsonify({})
