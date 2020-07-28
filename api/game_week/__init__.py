from flask import Blueprint

from .views import GameWeekView, CurrentGameWeekView

game_week_blueprint = Blueprint('game_weeks', __name__, url_prefix='/api/v1')
game_week_view = GameWeekView.as_view('game_week_api')
game_week_blueprint.add_url_rule(
    '/season/<season_id>/gameweeks/<game_week_id>', view_func=game_week_view,
    methods=['GET']
)
game_week_blueprint.add_url_rule(
    '/season/<season_id>/gameweeks', view_func=game_week_view,
    methods=['GET', 'POST']
)
game_week_blueprint.add_url_rule(
    '/gameweek/<game_week_id>', view_func=game_week_view,
    methods=['PUT', 'DELETE']
)

current_gameweek_view = CurrentGameWeekView.as_view('current_gameweek_api')
game_week_blueprint.add_url_rule(
    '/current_gameweek',
    view_func=current_gameweek_view,
    methods=['GET']
)
