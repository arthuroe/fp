from flask import Blueprint

from .views import PlayersView

players_blueprint = Blueprint('players', __name__, url_prefix='/api/v1')
players_view = PlayersView.as_view('players_api')
players_blueprint.add_url_rule(
    '/players', view_func=players_view, methods=['GET', 'POST']
)
players_blueprint.add_url_rule(
    '/players/<player_id>',
    view_func=players_view, methods=['GET', 'PUT', 'DELETE']
)
