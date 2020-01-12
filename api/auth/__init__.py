from flask import Blueprint

from api.auth.views import RegisterView, LoginView, UserView

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

user_view = UserView.as_view('user_api')
auth_blueprint.add_url_rule(
    '/current_user',
    view_func=user_view,
    methods=['GET']
)
