import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.auth.helpers import *
from api.models import User


class RegisterView(MethodView):
    """
    View to register a user
    """

    def post(self):
        post_data = request.json
        email = post_data.get('email')
        name = post_data.get('name')
        password = post_data.get('password')

        if not all([email, name, password]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. email, name and '
                            'password must be provided')
            }
            return make_response(jsonify(response)), 400

        if not validate_email(email) or not validate_password(password):
            response = {
                'status': 'fail',
                'message': ('Invalid Email or password provided'),
                'required': (
                    'Passwords should be at least 8 characters, contain'
                    ' a digit, uppercase and lowercase characters'
                )
            }
            return make_response(jsonify(response)), 400

        user = User.find_first(email=post_data.get('email'))
        if not user:
            try:
                user = User(email=email, password=password, name=name)
                user.save()

                auth_token = user.generate_token(user.id)
                response = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                logging.error(f"An error has occurred  {e}")
                response = {
                    'status': 'fail',
                    'message': 'Registration failed. Please try again.'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'fail',
                'message': 'User already exists. Please log in.',
            }
            return make_response(jsonify(response)), 409
