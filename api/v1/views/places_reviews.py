#!/usr/bin/python3
""" view for Places_reviews objects that handles all RESTFul API actions """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage

methods = ["GET", "PUT", "DELETE"]


@app_views.route(
        "/places/<place_id>/reviews", strict_slashes=False, methods=["GET"])
def place_reviews(place_id):
    """ handles all default RESTFul API actions """
    if place_id:
        place = storage.get(Place, place_id)

        if not place:
            abort(404)
        return jsonify([review.to_dict() for review in place.reviews])


@app_views.route(
        "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_reviews(place_id):
    """ method that handles POST request and creates a review object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    instance_data = request.get_json()
    if not instance_data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in instance_data:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, instance_data.get('user_id'))
    if not user:
        abort(404)

    if "text" not in instance_data:
        return jsonify({"error": "Missing text"}), 400

    instance_data["place_id"] = place_id
    review = Review(**instance_data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=methods)
def Reviews(review_id):
    """ Review method that handles GET, PUT, DELETE actions """
    if request.method == "GET":
        if review_id:
            review = storage.get(Review, review_id)

            if not review:
                abort(404)
            return jsonify(review.to_dict())

    if request.method == "DELETE":
        if review_id:
            review = storage.get(Review, review_id)

            if not review:
                abort(404)
            storage.delete(review)
            storage.save()
            return jsonify({}), 200

    if request.method == "PUT":
        if review_id:
            review = storage.get(Review, review_id)
            update_data = request.get_json()

            if not review:
                abort(404)
            if not update_data:
                return jsonify({"error": "Not a JSON"}), 400

            keys = ["id", "user_id", 'place_id', "created_at", "updated_at"]
            for key, value in update_data.items():
                if key not in keys:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict()), 200
