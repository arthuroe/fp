from flask import Blueprint

from .views import SeasonsView

seasons_blueprint = Blueprint('seasons', __name__, url_prefix='/api/v1')
season_view = SeasonsView.as_view('season_api')
seasons_blueprint.add_url_rule(
    '/seasons', defaults={'season_id': None},
    view_func=season_view,
    methods=['GET', 'POST']
)
