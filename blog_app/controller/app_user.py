from flask import json

from flask import Blueprint, request, jsonify, make_response, Response

from blog_app.controller import invalid_json_response, bcrypt
from blog_app.data import AppUser, db
from blog_app.service.app_user_service import get_user_by_username, \
    __generate_hash, Auth

user_api = Blueprint('app_user', __name__)


@user_api.route("/app_user", methods=["POST"])
def create_user():
    """
    Creates a user

    :return: the created user
    """
    data = request.get_json()
    try:
        app_user = AppUser(
            app_username=data["app_username"],
            user_password=__generate_hash(data["user_password"])
        )
    except KeyError as e:
        return invalid_json_response(f"missing property: {e}")
    user_in_db = get_user_by_username(data["app_username"])
    if user_in_db:
        return invalid_json_response(f"User: {data['app_username']} already exist")
    db.session.add(app_user)
    db.session.commit()
    db.session.refresh(app_user)
    token = Auth.generate_token(app_user.app_username)
    category_resource = jsonify({
        "id": app_user.id,
        "app_username": app_user.app_username,
        "user_password": app_user.user_password,
    })
    return token


