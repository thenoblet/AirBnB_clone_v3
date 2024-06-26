#!/usr/bin/python3
''''
Routes for managing State objects and operations.
'''
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    '''
    Retrieve all State objects.

    Returns:
    A JSON response containing all State objects.
    '''
    all_states = storage.all(State)
    all_states_dict = [state.to_dict() for state in all_states.values()]
    return jsonify(all_states_dict)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    '''
    Create a new State object.

    Returns:
    A JSON response containing the newly created State object.
    '''
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, 'Not a JSON')
    if "name" not in request_data:
        abort(400, 'Missing name')

    new_state = State(**request_data)
    new_state.save()
    response = jsonify(new_state.to_dict())
    response.status_code = 201
    return response


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    '''
    Retrieve a specific State object by ID.

    Args:
    state_id: The ID of the State object to retrieve.

    Returns:
    A JSON response containing the State object with the
    specified ID, or 404 if the State object was not found.
    '''
    state_instance = storage.get(State, state_id)
    if state_instance is None:
        abort(404)
    return jsonify(state_instance.to_dict())


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    '''
    Update a specific State object by ID.

    Args:
    state_id: The ID of the State object to update.

    Returns:
    A JSON response containing the updated State object on success
    (status code 200), or 404 if the State object was not found, or
    400 if the request body is not valid JSON.
    '''
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, 'Not a JSON')
    state_instance = storage.get(State, state_id)
    if state_instance is None:
        abort(404)
    for key, value in request_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_instance, key, value)
    state_instance.save()
    return jsonify(state_instance.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    '''
    Delete a State object by ID.

    Args:
    state_id: The ID of the State object to delete.

    Returns:
    An empty JSON response with status code 200 if the State was deleted
    successfully, or 404 if the State object was not found.
    '''
    state_instance = storage.get(State, state_id)
    if state_instance is None:
        abort(404)
    storage.delete(state_instance)
    storage.save()
    return jsonify({})
