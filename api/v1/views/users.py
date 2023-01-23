#!/usr/bin/python3
""" New view for User objects that handles default API actions """

from flask import Flask, Blueprint, jsonify, request, url_for, abort
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from models.user import User
import json


@app_views.route("/users/<string:user_id>", methods=['GET'],
                 strict_slashes=False)
def show_user_with_id(user_id):
    """ shows specific class with given id """

    data = storage.get(User, user_id)
    if data is None:
        abort(404)
    return jsonify(data.to_dict())


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def show_all_users():
    """ by default, shows all users """

    users = storage.all(User).values()
    new_list = []
    for user in users:
        new_list.append(user.to_dict())
    return jsonify(new_list)


@app_views.route("/users/<string:user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user_with_id(user_id):
    """ deletes the class associated with given id """

    data = storage.get(User, user_id)
    if data is None:
        abort(404)
    storage.delete(data)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def post_users():
    """ creates something new with parameters """

    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")

    obj = User(**data)
    storage.new(obj)
    storage.save()
    return obj.to_dict(), 201


@app_views.route("/users/<user_id>", methods=['PUT', 'GET'],
                 strict_slashes=False)
def put_users(user_id):
    """ updates class with information """

    data = storage.get(User, user_id)

    if not data:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")

    my_req = request.get_json()

    for k, v in my_req.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(data, k, v)

    storage.save()
    return data.to_dict(), 200
