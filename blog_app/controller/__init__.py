from flask import make_response, jsonify
from flask_bcrypt import Bcrypt


def invalid_json_response(body):
    return make_response(jsonify({"bad_request": body}), 400)

bcrypt = Bcrypt()