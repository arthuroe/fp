from flask import Blueprint

from .views import GameWeekView

game_week_blueprint = Blueprint('game_weeks', __name__, url_prefix='/api/v1')
game_week_view = GameWeekView.as_view('game_week_api')
game_week_blueprint.add_url_rule(
    '/game_week', view_func=game_week_view, methods=['GET', 'POST']
)
