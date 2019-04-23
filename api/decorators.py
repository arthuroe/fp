from flask import request, jsonify, make_response
from functools import wraps

from api.models import User


def token_required(func):
    """
    Decorator function to ensure that a resource is access by only
    authenticated users provided their auth tokens are valid
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'Provide a valid auth token'
                })), 403

        if not token:
            return make_response(jsonify({
                'status': 'failed',
                'message': 'Token is missing'
            })), 401

        try:
            decode_response = User.decode_token(token)
            current_user = User.query.filter_by(id=decode_response).first()
        except:
            message = 'Invalid token'
            if isinstance(decode_response, str):
                message = decode_response
            return make_response(jsonify({
                'status': 'failed',
                'message': message
            })), 401
        return func(current_user, *args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        admin = current_user.is_admin
        if roles:
            return f(*args, **kwargs)

        response = jsonify({
            "status": "fail",
            "data": {
                "message": "You are not authorized to carry out this operation",
            }
        })
        response.status_code = 401
        return response

    return decorated
