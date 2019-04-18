from flask import Blueprint

from api.auth.views import RegisterView

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1')
registration_view = RegisterView.as_view('register_api')
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
