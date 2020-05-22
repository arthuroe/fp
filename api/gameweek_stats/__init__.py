from flask import Blueprint

from .views import GameWeekStatsView

gameweek_stats_blueprint = Blueprint(
    'gameweek_stats', __name__, url_prefix='/api/v1')
gameweek_stats_view = GameWeekStatsView.as_view('gameweek_stats_api')
game_week_blueprint.add_url_rule(
    '/gameweek_stats', view_func=gameweek_stats_view, methods=['GET'])
