import datetime
import os
from functools import wraps

import jwt
from flask import Response, request, current_app

from blog_app.controller import bcrypt, invalid_json_response
from blog_app.data import AppUser, db

from flask import json


def __generate_hash(password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")


def check_hash(pw_hash, password):
    #xx = check_hash(user_in_db.user_password, data["user_password"])
    return bcrypt.check_password_hash(pw_hash, password)


def get_user_by_username(username):
    return db.session.query(AppUser).filter(AppUser.app_username == username).first()


def get_user_by_id(user_id):
    return db.session.query(AppUser).filter(AppUser.id == user_id).first()


class Auth:
    @staticmethod
    def generate_token(username):
        """
        Generate Token Method
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': username
            }
            return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256').decode("utf-8")
        except Exception as e:
            return invalid_json_response(f" error in generating user token: {e}")

    @staticmethod
    def decode_token(token):
        """
        Decode token method
        """
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'])
            re['data'] = {'id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'token expired, please login again'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {
                'message': 'Invalid token, please try again with a new token'}
            return re

    @staticmethod
    def auth_required(func):
        """
        Auth decorator
        """
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return invalid_json_response('Authentication token is not '
                                             'available, please login to '
                                             'get one')
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )

            user_id = data['data']['id']
            check_user = get_user_by_id(user_id)
            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(
                        {'error': 'user does not exist, invalid token'}),
                    status=400
                )
            g.user = {'id': user_id}
            return func(*args, **kwargs)

        return decorated_auth
