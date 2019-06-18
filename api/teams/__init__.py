from flask import Blueprint

from .views import TeamsView

teams_blueprint = Blueprint('teams', __name__, url_prefix='/api/v1')
teams_view = TeamsView.as_view('team_api')
teams_blueprint.add_url_rule(
    '/teams', view_func=teams_view, methods=['GET', 'POST']
)
teams_blueprint.add_url_rule(
    '/teams/<team_id>', view_func=teams_view, methods=['PUT', 'DELETE']
)
