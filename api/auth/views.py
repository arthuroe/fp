import logging
import os
import urllib.parse

from flask import (
    Blueprint, request, redirect, make_response, jsonify, render_template)
from flask.views import MethodView
from flask.wrappers import Response

from api.auth.helpers import *
from api.decorators import token_required
from api.email import send_email
from api.models import User


class RegisterView(MethodView):
    """
    View to register a user
    """

    def post(self):
        post_data = request.json
        email = post_data.get('email')
        first_name = post_data.get('first_name')
        password = post_data.get('password')

        if not all([email, first_name, password]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. email, first_name and '
                            'password must be provided')
            }
            return make_response(jsonify(response)), 400

        if not validate_email(email) or not validate_password(password):
            response = {
                'status': 'fail',
                'message': 'Invalid Email or password provided',
                'required': (
                    'Passwords should be at least 8 characters, contain'
                    ' a digit, uppercase and lowercase characters'
                )
            }
            return make_response(jsonify(response)), 400

        user = User.find_first(email=post_data.get('email'))
        if not user:
            try:
                user = User(**post_data)
                user_teams = get_user_teams(post_data.get('favorite_clubs'))
                user.favorite_clubs.extend(user_teams)
                user.save()

                response = {
                    'status': 'success',
                    'message': 'Successfully registered.'
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


class LoginView(MethodView):
    """
    View to login the user
    """

    def post(self):
        try:
            post_data = request.json
            email = post_data.get('email')
            password = post_data.get('password')

            if not email or not password:
                response = {
                    'status': 'fail',
                    'message': 'email or password not provided.'
                }
                return make_response(jsonify(response)), 400

            if not validate_email(email):
                response = {
                    'status': 'fail',
                    'message': 'Invalid email or password provided'
                }
                return make_response(jsonify(response)), 400

            user = User.find_first(email=email)

            if user and not user.password_is_valid(password):
                response = {
                    'status': 'fail',
                    'message': 'Invalid email or password provided'
                }
                return make_response(jsonify(response)), 401

            if user and user.password_is_valid(password):
                auth_token = user.generate_token(user.id)
                if auth_token:
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response)), 401
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'An error has occurred. Please try again.'
            }
            return make_response(jsonify(response)), 500


class ChangePasswordView(MethodView):
    """
    View to change user password
    """
    decorators = [token_required]

    def post(self, current_user):
        kwargs = request.json
        current_password = kwargs.get('current_password')
        new_password = kwargs.get('new_password')

        try:
            user = User.find_first(id=current_user.id)

            if not validate_password(new_password):
                response = {
                    'status': 'fail',
                    'message': 'Invalid password provided',
                    'required': (
                        'Passwords should be at least 8 characters, contain'
                        ' a digit, uppercase and lowercase characters'
                    )
                }
                return make_response(jsonify(response)), 400

            if not user.password_is_valid(current_password):
                response = {
                    'status': 'fail',
                    'message': 'Invalid current password provided.'
                }
                return make_response(jsonify(response)), 400

            if current_password == new_password:
                response = {
                    'status': 'fail',
                    'meassge': 'Current password and new password should not match.'
                }
                return make_response(jsonify(response)), 400

            password = user.hash_password(new_password)
            user.update(password=password, id=current_user.id)
            response = {
                'status': 'success',
                'meassge': 'Password successfully updated.'
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update password please try again.'
            }
            return make_response(jsonify(response)), 500



class ResetPasswordView(MethodView):
    """
    View to reset user password
    """

    def get(self, token):
        if confirm_token(token):
            email = confirm_token(token)
            user = User.find_first(email=email)
            token = user.generate_token(user.id)
            base_url = os.getenv('FRONT_END_URL')
            return (
                "", 302,
                {
                    "location": f"{base_url}/resetpassword?token={token}",
                    "Authorization": token
                }
            )

        response = {
            'status': 'fail',
            'meassge': 'Expired or invalid url.'
        }
        return make_response(jsonify(response)), 400

    def post(self):
        email = request.json.get('email')
        try:
            user = User.find_first(email=email)
            if not user:
                return make_response(jsonify({'message': 'No user information found'})), 404

            token = generate_confirmation_token(email)
            url = generate_reset_url(request.headers.get('host'), token)
            html = render_template(
                'reset.html', username=user.first_name, url=url)
            subject = "Reset your password"
            send_email(subject, [user.email], 'Reset Password', html)
            response = {
                'status': 'success',
                'meassge': 'Instructions have been sent to your email.'
            }
            return make_response(jsonify(response)), 200
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to send email.'
            }
            return make_response(jsonify(response)), 500


class UpdatePasswordView(MethodView):
    """
    View to update user password
    """
    decorators = [token_required]

    def put(self, current_user):
        kwargs = request.json
        password = kwargs.get('password')
        confirm_password = kwargs.get('confirm_password')

        try:
            user = User.find_first(id=current_user.id)

            if not validate_password(password):
                response = {
                    'status': 'fail',
                    'message': 'Invalid password provided',
                    'required': (
                        'Passwords should be at least 8 characters, contain'
                        ' a digit, uppercase and lowercase characters'
                    )
                }
                return make_response(jsonify(response)), 400


            if password != confirm_password:
                response = {
                    'status': 'fail',
                    'meassge': 'password and confirmed password do not match.'
                }
                return make_response(jsonify(response)), 400

            password = user.hash_password(password)
            user.update(password=password, id=current_user.id)
            response = {
                'status': 'success',
                'meassge': 'Password successfully updated.'
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update password please try again.'
            }
            return make_response(jsonify(response)), 500
