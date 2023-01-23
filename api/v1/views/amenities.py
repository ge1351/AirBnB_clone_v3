#!/usr/bin/python3

"""this is the amenities module"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def show_all_amenities():
    """shows all amenities"""

    amenities = storage.all(Amenity)
    new_list = []
    for amenity in amenities.values():
        new_list.append(amenity.to_dict())
    return jsonify(new_list)


@app_views.route("/amenities/<string:amenity_id>", methods=['GET'],
                 strict_slashes=False)
def show_amenity_with_id(amenity_id):
    """shows amenity with given id"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_with_id(amenity_id):
    """deletes amenity with given id"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates amenity"""

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity_with_id(amenity_id):
    """updates amenity with given id"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
