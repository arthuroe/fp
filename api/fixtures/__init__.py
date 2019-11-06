from flask import Blueprint

from .views import FixturesView

fixtures_blueprint = Blueprint('fixtures', __name__, url_prefix='/api/v1')
fixtures_view = FixturesView.as_view('fixtures_api')
fixtures_blueprint.add_url_rule(
    '/fixtures', view_func=fixtures_view, methods=['GET'])
fixtures_blueprint.add_url_rule(
    '/fixtures/<season_id>', view_func=fixtures_view, methods=['GET', 'POST'])
