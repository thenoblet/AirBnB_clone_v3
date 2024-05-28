#!/usr/bin/python3
'''
Routes for managing User objects and operations.
'''
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    '''
    Retrieve the list of all User objects.

    Returns:
    A JSON response containing all User objects.
    '''
    all_users = storage.all(User)
    all_users_dict = [user.to_dict() for user in all_users.values()]
    return jsonify(all_users_dict)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    '''
    Retrieve a specific User object by ID.

    Args:
    user_id: The ID of the User object to retrieve.

    Returns:
    A JSON response containing the User object with the specified ID,
    or 404 if the User object was not found.
    '''
    user_instance = storage.get(User, user_id)
    if user_instance is None:
        abort(404)
    return jsonify(user_instance.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''
    Create a new User object.

    Returns:
    A JSON response containing the newly created User object.
    '''
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, 'Not a JSON')
    if 'email' not in request_data:
        abort(400, 'Missing email')
    if 'password' not in request_data:
        abort(400, 'Missing password')

    new_user = User(**request_data)
    new_user.save()
    response = jsonify(new_user.to_dict())
    response.status_code = 201
    return response


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
    Update a specific User object by ID.

    Args:
    user_id: The ID of the User object to update.

    Returns:
    A JSON response containing the updated User object on success
    (status code 200), or 404 if the User object was not found, or
    400 if the request body is not valid JSON.
    '''
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, 'Not a JSON')
    user_instance = storage.get(User, user_id)
    if user_instance is None:
        abort(404)
    for key, value in request_data.items():
        if key not in ['id', 'email', 'password', 'created_at', 'updated_at']:
            setattr(user_instance, key, value)
    user_instance.save()
    return jsonify(user_instance.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id):
    '''
    Delete a User object by ID.

    Args:
    user_id: The ID of the User object to delete.

    Returns:
    An empty JSON response with status code 200 if the User was deleted
    successfully, or 404 if the User object was not found.
    '''
    user_instance = storage.get(User, user_id)
    if user_instance is None:
        abort(404)
    storage.delete(user_instance)
    storage.save()
    return jsonify({})
