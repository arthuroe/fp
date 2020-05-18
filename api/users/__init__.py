from flask import Blueprint

from api.users.views import ManageUserView, UserView

user_blueprint = Blueprint('users', __name__, url_prefix='/api/v1')
manage_user_view = ManageUserView.as_view('manageuser_api')
user_blueprint.add_url_rule(
    '/users',
    view_func=manage_user_view,
    methods=['GET', 'POST']
)
user_blueprint.add_url_rule(
    '/users/<user_id>',
    view_func=manage_user_view,
    methods=['GET', 'DELETE']
)

user_view = UserView.as_view('user_api')
user_blueprint.add_url_rule(
    '/current_user',
    view_func=user_view,
    methods=['GET']
)
user_blueprint.add_url_rule(
    '/users/<user_id>',
    view_func=user_view,
    methods=['PUT']
)
