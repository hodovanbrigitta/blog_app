from flask import Blueprint, request, jsonify, make_response, g

from blog_app.controller import invalid_json_response
from blog_app.service import save
from blog_app.service.app_user_service import get_user_by_username, \
    generate_hash, check_hash, get_all_users, get_user_by_id, \
    create_user
from blog_app.service.authentication import auth

user_api = Blueprint('app_user', __name__)


@user_api.route("/app_user", methods=["GET"])
def get_app_users():
    """
    Returns every users from our application

    :return: every user from our application
    """
    user_models = get_all_users()
    return jsonify([{
        "id": app_user.id,
        "app_username": app_user.app_username,
        "user_password": app_user.user_password
    } for app_user in user_models])


@user_api.route("/app_user/me", methods=["GET"])
def get_me():
    """
    Returns the basic data about the actual user
    :return: a user from our application
    """
    app_user = get_user_by_id(g.user.get('user_id'))
    if app_user is None:
        return invalid_json_response(
            f"user with ID {g.user.get('user_id')} does not exist")
    return jsonify({
        "id": app_user.id,
        "app_username": app_user.app_username,
        "user_password": app_user.user_password
    })


@user_api.route("/app_user/<user_id>", methods=["GET"])
def get_app_user(user_id):
    """
    Returns a user from our application with the given ID

    :param user_id: the user's ID to return
    :return: a user from our application with the given ID
    """
    try:
        user_id = int(user_id)
    except ValueError:
        return invalid_json_response("invalid input type")
    app_user = get_user_by_id(user_id)
    if app_user is None:
        return invalid_json_response(
            f"user with ID {user_id} does not exist")
    return jsonify({
        "id": app_user.id,
        "app_username": app_user.app_username,
        "user_password": app_user.user_password
    })


@user_api.route("/app_user", methods=["POST"])
def create_new_user():
    """
    Creates a user

    :return: the created user
    """
    data = request.get_json()
    try:
        app_user = create_user(data["app_username"],
                               generate_hash(data["user_password"]))
    except KeyError as e:
        return invalid_json_response(f"missing property: {e}")
    user_in_db = get_user_by_username(data["app_username"])

    if user_in_db:
        return invalid_json_response(f"User: {data['app_username']} "
                                     f"already exist")
    save(app_user)
    token = auth.generate_token(app_user.id)
    res_token = jsonify({
        "jwt-token": token,
        "id": app_user.id,
        "app_username": app_user.app_username,
        "user_password": app_user.user_password
    })
    return make_response(res_token, 201)


@user_api.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    try:
        actual_user = create_user(data["app_username"], data["user_password"])
    except KeyError as e:
        return invalid_json_response(f"missing property: {e}")

    user_in_db = get_user_by_username(actual_user.app_username)

    if not user_in_db:
        # TODO do not expose existing usernames
        return invalid_json_response(
            f"user with username {data['app_username']} does not exist")

    if not check_hash(user_in_db.user_password, data["user_password"]):
        return invalid_json_response(f"invalid password")

    token = auth.generate_token(user_in_db.id)

    res_token = jsonify({
        "jwt-token": token,
        "id": user_in_db.id,
        "app_username": user_in_db.app_username,
        "user_password": user_in_db.user_password
    })
    return make_response(res_token, 200)
