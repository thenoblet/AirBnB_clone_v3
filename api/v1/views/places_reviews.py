#!/usr/bin/python3
'''
Routes for managing Review objects and operations.
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    '''
    Retrieve the list of all Review objects for a specific Place.

    Args:
    place_id: The ID of the Place.

    Returns:
    A JSON response containing all Review objects for the specified Place.
    '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    '''
    Retrieve a specific Review object by ID.

    Args:
    review_id: The ID of the Review object to retrieve.

    Returns:
    A JSON response containing the Review object with the specified ID,
    or 404 if the Review object was not found.
    '''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''
    Create a new Review object for a specific Place.

    Args:
    place_id: The ID of the Place.

    Returns:
    A JSON response containing the newly created Review object,
    or appropriate error responses.
    '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_data:
        abort(400, 'Missing user_id')
    if 'text' not in request_data:
        abort(400, 'Missing text')

    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)

    new_review = Review(**request_data)
    new_review.place_id = place_id
    new_review.save()
    response = jsonify(new_review.to_dict())
    response.status_code = 201
    return response


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''
    Update a specific Review object by ID.

    Args:
    review_id: The ID of the Review object to update.

    Returns:
    A JSON response containing the updated Review object on success,
    or appropriate error responses.
    '''
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    for key, value in request_data.items():
        if key not in [
                'id', 'user_id', 'place_id', 'created_at', 'updated_at'
        ]:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''
    Delete a Review object by ID.

    Args:
    review_id: The ID of the Review object to delete.

    Returns:
    An empty JSON response with status code 200 if the Review was deleted
    successfully, or 404 if the Review object was not found.
    '''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({})
