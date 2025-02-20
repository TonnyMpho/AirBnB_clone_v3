#!/usr/bin/python3
""" view for State objects that handles all default RESTFul API actions """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from models import storage

methods = ["GET", "DELETE", "POST", "PUT"]


@app_views.route("/users", strict_slashes=False, methods=methods)
@app_views.route("/users/<user_id>", methods=methods)
def users(user_id=None):
    """ handles all default RESTFul API actions """
    if request.method == "GET":
        if user_id:
            user = storage.get(User, user_id)

            if not user:
                abort(404)
            return jsonify(user.to_dict())
        else:
            users = storage.all(User).values()
            return jsonify([user.to_dict() for user in users])

    elif request.method == "DELETE":
        if user_id:
            user = storage.get(User, user_id)
            if not user:
                abort(404)
            storage.delete(user)
            storage.save()
            return jsonify({}), 200

    elif request.method == "POST":
        instance = request.get_json()

        if not instance:
            return jsonify({"error": "Not a JSON"}), 400
        if "email" not in instance:
            return jsonify({"error": "Missing email"}), 400
        if "password" not in instance:
            return jsonify({"error": "Missing password"}), 400

        user = User(**instance)
        user.save()
        return jsonify(user.to_dict()), 201

    elif request.method == "PUT":
        if user_id:
            user = storage.get(User, user_id)

            if user is None:
                abort(404)

            update_data = request.get_json()
            if update_data is None:
                return jsonify({"error": "Not a JSON"}), 400

            for key, value in update_data.items():
                if key not in ['id', 'email', 'created_at', 'updated_at']:
                    setattr(user, key, value)

            user.save()
            return jsonify(user.to_dict()), 200
