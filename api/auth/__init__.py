from flask import Blueprint

from api.auth.views import RegisterView, LoginView

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
