import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required
from api.models import Fixture, GameWeek


class FixturesView(MethodView):
    """
    View to handle Fixturess
    """

    def get(self, game_week_id=None):
        if game_week_id:
            fixture = Fixture.find_first(game_week_id=game_week_id)
            if not game_week_id:
                response = {
                    'status': 'fail',
                    'message': 'GameWeek does not exist'
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

    def post(self, game_week_id):
        kwargs = request.json()
        kwargs.update({"game_week_id": game_week_id})
        try:
            fixture = Fixture(**kwargs)
            game_week = GameWeek.find_first(id=game_week_id)

            if not game_week:
                response = {
                    'status': 'fail',
                    'message': 'GameWeek does not exist'
                }
                return make_response(jsonify(response)), 400

            if fixture in game_week.fixtures:
                response = {
                    'status': 'fail',
                    'message': 'Fixture already added to GameWeek.'
                }
                return make_response(jsonify(response)), 400

            game_week.fixtures.append(fixture)
            fixture.save()
            response = {
                'status': 'success',
                'message': f"Successfully added {kwargs.get('home_name')} vs "
                f"{kwargs.get('away_name')}"
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add fixture.'
            }
            return make_response(jsonify(response)), 400
