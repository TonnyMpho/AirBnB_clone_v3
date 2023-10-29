#!/usr/bin/python3
""" view for State objects that handles all default RESTFul API actions """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states", strict_slashes=False, methods=["GET", "DELETE", "POST", "PUT"])
@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "POST", "PUT"])
def states(state_id=None):
    """ handles all default RESTFul API actions """
    if request.method == "GET":
        if state_id:
            state = storage.get(State, state_id)

            if not state:
                abort(404)
            return jsonify(state.to_dict())
        else:
            states = storage.all(State).values()
            return jsonify([state.to_dict() for state in states])

    elif request.method == "DELETE":
        if stae_id:
            state = storage.get(State, state_id)
            if not state:
                abort(404)
            storage.delete(state)
            storage.save()
            return jsonify({}), 200

    elif request.method == "POST":
        instance = request.get_json()

        if not instance:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in instance:
            return jsonify({"error": "Missing name"}), 400

        state = State(**instance)
        state.save()
        return jsonify(state.to_dict()), 201

    elif request.method == "PUT":
        if state_id:
            state = storage.get(State, state_id)

            if state is None:
                abort(404)

            update_data = request.get_json()
            if update_data is None:
                return jsonify({"error": "Not a JSON"}), 400

            for key, value in update_data:
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(state, key, value)

            state.save()
            return jsonify(state.to_dict()), 200
