from flask import make_response, jsonify
from flask_bcrypt import Bcrypt

from blog_app.data import db


def invalid_json_response(body):
    return make_response(jsonify({"bad_request": body}), 400)


def save(self):
    db.session.add(self)
    db.session.commit()
    db.session.refresh(self)


def delete(self):
    db.session.delete(self)
    db.session.commit()


bcrypt = Bcrypt()