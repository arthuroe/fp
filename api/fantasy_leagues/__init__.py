from flask import Blueprint

from .views import FantasyLeagueView, FantasyLeagueUsersView

fantasy_league_blueprint = Blueprint(
    'fantasy_leagues', __name__, url_prefix='/api/v1')
fantasy_league_view = FantasyLeagueView.as_view('fantasy_leagues_api')
fantasy_league_blueprint.add_url_rule(
    '/fantasy_leagues', view_func=fantasy_league_view, methods=['GET', 'POST']
)

fantasy_league_user_view = FantasyLeagueUsersView.as_view(
    'fantasy_leagues_users_api')
fantasy_league_blueprint.add_url_rule(
    '/join_fantasy_league', view_func=fantasy_league_user_view, methods=['POST']
)
fantasy_league_blueprint.add_url_rule(
    '/view_fantasy_league/<fantasy_league_id>',
    view_func=fantasy_league_user_view, methods=['GET']
)
