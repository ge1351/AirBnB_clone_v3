#!/usr/bin/python3
""" this is a module to handle reviews"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def get_place_reviews(place_id):
    """all revirews"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([rev.to_dict() for rev in place.reviews])


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_review(review_id):
    """revierwa by id"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete review by id"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a new review"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    user = storage.get("User", data['user_id'])
    if not user:
        abort(404)
    review = Review(**data)
    review.place_id = place_id
    review.user_id = data['user_id']
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update review by id"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' in data:
        user = storage.get("User", data['user_id'])
        if not user:
            abort(404)
        review.user_id = data['user_id']
    if 'text' in data:
        review.text = data['text']
    if 'place_id' in data:
        place = storage.get("Place", data['place_id'])
        if not place:
            abort(404)
        review.place_id = data['place_id']
    review.save()
    return jsonify(review.to_dict()), 200
