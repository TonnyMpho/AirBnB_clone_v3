#!/usr/bin/python3
""" view for City objects that handles all default RESTFul API actions """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models import storage

methods = ["GET", "PUT", "DELETE"]


@app_views.route("/cities/<city_id>/places", strict_slashes=False, methods=["GET"])
def city_places(city_id):
    """ handles all default RESTFul API actions """
    if city_id:
        city = storage.get(City, city_id)

        if not city:
            abort(404)
        return jsonify([place.to_dict() for place in city.places])


@app_views.route(
        "/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """ method that handles POST request and craetes a city object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    instance_data = request.get_json()
    if not instance_data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in instance_data:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get('User', instance_data.get('user_id'))
    if not user:
        abort(404)

    if "name" not in instance_data:
        return jsonify({"error": "Missing name"}), 400


    instance_data["city_id"] = city_id
    place = Place(**instance_data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=methods)
def places(place_id):
    """ City method that handles GET, PUT, DELETE actions """
    if request.method == "GET":
        if place_id:
            place = storage.get(Place, place_id)

            if not place:
                abort(404)
            return jsonify(place.to_dict())

    if request.method == "DELETE":
        if place_id:
            place = storage.get(Place, place_id)

            if not place:
                abort(404)
            storage.delete(place)
            storage.save()
            return jsonify({}), 200

    if request.method == "PUT":
        if place_id:
            place = storage.get(Place, place_id)
            update_data = request.get_json()

            if not place:
                abort(404)
            if not update_data:
                return jsonify({"error": "Not a JSON"}), 400

            for key, value in update_data.items():
                if key not in ["id", "city_id", "created_at", "updated_at"]:
                    setattr(place, key, value)
            place.save()
            return jsonify(place.to_dict()), 200
