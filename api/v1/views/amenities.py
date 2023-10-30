#!/usr/bin/python3
""" view for Amenities objects that handles all default RESTFul API actions """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage

methods = ["GET", "DELETE", "POST", "PUT"]


@app_views.route("/amenities", strict_slashes=False, methods=methods)
@app_views.route("/amenities/<amenity_id>", methods=methods)
def amenities(amenity_id=None):
    """ handles all default RESTFul API actions """
    if request.method == "GET":
        if amenity_id:
            amenity = storage.get(Amenity, amenity_id)

            if not amenity:
                abort(404)
            return jsonify(amenity.to_dict())
        else:
            amenities = storage.all(Amenity).values()
            return jsonify([amenity.to_dict() for amenity in amenities])

    elif request.method == "DELETE":
        if amenity_id:
            amenity = storage.get(Amenity, amenity_id)
            if not amenity:
                abort(404)
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200

    elif request.method == "POST":
        instance = request.get_json()

        if not instance:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in instance:
            return jsonify({"error": "Missing name"}), 400

        amenity = Amenity(**instance)
        amenity.save()
        return jsonify(amenity.to_dict()), 201

    elif request.method == "PUT":
        if amenity_id:
            amenity = storage.get(Amenity, amenity_id)

            if amenity is None:
                abort(404)

            update_data = request.get_json()
            if update_data is None:
                return jsonify({"error": "Not a JSON"}), 400

            for key, value in update_data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(amenity, key, value)

            amenity.save()
            return jsonify(amenity.to_dict()), 200
