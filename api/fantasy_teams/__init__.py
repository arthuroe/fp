from flask import Blueprint

from .views import FantasyTeamView

fantasy_team_blueprint = Blueprint(
    'fantasy_teams', __name__, url_prefix='/api/v1')
fantasy_team_view = FantasyTeamView.as_view('fantasy_team_api')
