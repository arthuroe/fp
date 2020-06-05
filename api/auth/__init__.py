from flask import Blueprint

from api.auth.views import (
    RegisterView, LoginView, ChangePasswordView, ResetPasswordView)

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1')
registration_view = RegisterView.as_view('register_api')
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)

login_view = LoginView.as_view('login_api')
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)

change_password_view = ChangePasswordView.as_view('change_password_api')
auth_blueprint.add_url_rule(
    '/auth/change_password',
    view_func=change_password_view,
    methods=['POST']
)

reset_password_view = ResetPasswordView.as_view('reset_password_api')
auth_blueprint.add_url_rule(
    '/auth/reset_password',
    view_func=reset_password_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/reset_password/<token>',
    view_func=reset_password_view,
    methods=['GET']
)
