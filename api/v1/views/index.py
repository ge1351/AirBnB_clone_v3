#!/usr/bin/python3
"""Creates a route that returns a JSON"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def return_jsonify():
    """Returns JSON status=OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def endpoint():
    """Retrieves number of each object by type"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    return jsonify({
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
        })
