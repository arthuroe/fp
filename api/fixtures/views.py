import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required
from api.models import Fixture


class FixturesView(MethodView):
    """
    View to handle Fixturess
    """

    def get(self, season_id=None):
        if season_id:
            fixture = Fixture.find_first(season_id=season_id)
            if not season_id:
                response = {
                    'status': 'fail',
                    'message': 'Season does not exist'
                }
                return make_response(jsonify(response)), 400
            response = {
                'status': 'success',
                'fixture': fixture.serialize()
            }
            return make_response(jsonify(response)), 200

        fixtures = Fixture.fetch_all()
        if not fixtures:
            response = {
                'status': 'success',
                'message': 'No fixtures have been added'
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'fixtures': [fixture.serialize() for fixture in fixtures]
        }
        return make_response(jsonify(response)), 200

    def post(self):
        pass
