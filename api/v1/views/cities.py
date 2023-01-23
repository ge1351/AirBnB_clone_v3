#!/usr/bin/python3

""" this is a module that lets us import all our views """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def show_all_cities_with_state_id(state_id):
    """ shows all cities with given state id """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    new_list = []
    for city in cities:
        new_list.append(city.to_dict())
    return jsonify(new_list)


@app_views.route("/cities/<string:city_id>", methods=['GET'],
                 strict_slashes=False)
def show_city_with_id(city_id):
    """ shows city with given id """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city_with_id(city_id):
    """ deletes city with given id """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<string:state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city_with_state_id(state_id):
    """ creates city with given state id """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city_with_id(city_id):
    """ updates city with given id """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
