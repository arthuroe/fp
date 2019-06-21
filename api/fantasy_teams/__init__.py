from flask import Blueprint

from .views import FantasyTeamView

fantasy_team_blueprint = Blueprint(
    'fantasy_teams', __name__, url_prefix='/api/v1')
fantasy_team_view = FantasyTeamView.as_view('fantasy_team_api')
fantasy_team_blueprint.add_url_rule(
    '/fantasy_teams', view_func=fantasy_team_view, methods=['GET', 'POST'])
