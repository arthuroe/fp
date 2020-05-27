from flask import Blueprint

from .views import GameWeekStatsView

gameweek_stats_blueprint = Blueprint(
    'gameweek_stats', __name__, url_prefix='/api/v1')
gameweek_stats_view = GameWeekStatsView.as_view('gameweek_stats_api')
gameweek_stats_blueprint.add_url_rule(
    '/gameweek_stats/<game_week_id>', view_func=gameweek_stats_view,
    methods=['GET']
)
gameweek_stats_blueprint.add_url_rule(
    '/gameweek_stats/<game_week_id>/<player_id>', view_func=gameweek_stats_view,
    methods=['GET', 'POST']
)
