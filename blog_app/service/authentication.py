import datetime
from functools import wraps

import jwt
from flask import Response, request, current_app, g
from flask import json

from blog_app.controller import invalid_json_response
from blog_app.service.app_user import get_user_by_id


class Authentication:
    def generate_token(self, user_id):
        """
        Generate Token Method
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'],
                              algorithm='HS256').decode("utf-8")
        except Exception as e:
            return invalid_json_response(
                f" error in generating user token: {e}")

    def decode_token(self, token):
        """
        Decode token method
        """
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'])
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError:
            re['error'] = {'message': 'token expired, please login again'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {
                'message': 'Invalid token, please try again with a new token'}
            return re

    def auth_required(self, func):
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
            data = auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )

            user_id = data['data']['user_id']
            check_user = get_user_by_id(user_id)
            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(
                        {'error': 'user does not exist, invalid token'}),
                    status=400
                )
            g.user = {'user_id': user_id}
            return func(*args, **kwargs)

        return decorated_auth


auth = Authentication()
