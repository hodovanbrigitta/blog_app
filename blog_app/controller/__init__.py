from flask import make_response, jsonify


def invalid_json_response(body):
    return make_response(jsonify({"bad_request": body}), 400)
