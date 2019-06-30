from flask import Blueprint

from .views import FantasyLeagueView

fantasy_league_blueprint = Blueprint(
    'fantasy_leagues', __name__, url_prefix='/api/v1')
fantasy_league_view = FantasyLeagueView.as_view('fantasy_leagues_api')
fantasy_league_blueprint.add_url_rule(
    '/fantasy_leagues', view_func=fantasy_league_view, methods=['GET', 'POST']
)
