from flask import Blueprint

from .views import SeasonsView, CurrentSeasonView

seasons_blueprint = Blueprint('seasons', __name__, url_prefix='/api/v1')
season_view = SeasonsView.as_view('season_api')
current_season_view = CurrentSeasonView.as_view('current_season_api')
seasons_blueprint.add_url_rule(
    '/seasons', view_func=season_view, methods=['GET', 'POST']
)
seasons_blueprint.add_url_rule(
    '/seasons/<season_id>',
    view_func=season_view, methods=['GET', 'PUT', 'DELETE']
)
seasons_blueprint.add_url_rule(
    '/seasons/current_season',
    view_func=current_season_view, methods=['GET']
)
