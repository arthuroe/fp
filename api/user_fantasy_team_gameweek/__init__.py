from flask import Blueprint

from api.user_fantasy_team_gameweek.views import UserFantasyTeamGameWeekView

user_fantasy_team_gameweek_blueprint = Blueprint('user_fantasy_gameweek', __name__, url_prefix='/api/v1')
user_fantasy_gameweek_view = UserFantasyTeamGameWeekView.as_view('user_fantasy_gameweek_api')

user_fantasy_team_gameweek_blueprint.add_url_rule(
    '/user-fantasy-gameweek/<game_week_id>', view_func=user_fantasy_gameweek_view, methods=['POST', 'GET'])


