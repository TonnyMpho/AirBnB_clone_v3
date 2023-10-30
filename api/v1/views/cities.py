#!/usr/bin/python3
""" view for City objects that handles all default RESTFul API actions """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage

methods = ["GET", "PUT", "DELETE"]


@app_views.route(
        "/states/<state_id>/cities", strict_slashes=False, methods=["GET"])
def state_cities(state_id=None):
    """ handles all default RESTFul API actions """
    if state_id:
        state = storage.get(State, state_id)

        if not state:
            abort(404)
        return jsonify([city.to_dict() for city in state.cities])


@app_views.route(
        "/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """ method that handles POST request and craetes a city object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    instance_data = request.get_json()
    if not instance_data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in instance_data:
        return jsonify({"error": "Missing name"}), 400

    instance_data["state_id"] = state_id
    city = City(**instance_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=methods)
def cities(city_id):
    """ City method that handles GET, PUT, DELETE actions """
    if request.method == "GET":
        if city_id:
            city = storage.get(City, city_id)

            if not city:
                abort(404)
            return jsonify(city.to_dict())

    if request.method == "DELETE":
        if city_id:
            city = storage.get(City, city_id)

            if not city:
                abort(404)
            storage.delete(city)
            storage.save()
            return jsonify({}), 200

    if request.method == "PUT":
        if city_id:
            city = storage.get(City, city_id)
            update_data = request.get_json()

            if not city:
                abort(404)
            if not update_data:
                return jsonify({"error": "Not a JSON"}), 400

            for key, value in update_data.items():
                if key not in ["id", "state_id", "created_at", "updated_at"]:
                    setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
