import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import admin_required, token_required
from api.models import Fixture, GameWeek


class FixturesView(MethodView):
    """
    View to handle Fixturess
    """

    @token_required
    def get(self, current_user, game_week_id=None):
        if game_week_id:
            fixture = Fixture.find_first(game_week_id=game_week_id)
            if not game_week_id:
                response = {
                    'status': 'fail',
                    'message': 'Fixture does not exist'
                }
                return make_response(jsonify(response)), 404
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

    @token_required
    @admin_required
    def post(self, current_user, game_week_id):
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
                return make_response(jsonify(response)), 404

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
            return make_response(jsonify(response)), 500

    @token_required
    @admin_required
    def put(self, current_user, fixture_id):
        kwargs = request.json()
        kwargs.update({"id": fixture_id})
        try:
            fixture = Fixture.find_first(id=fixture_id)
            if not fixture:
                response = {
                    'status': 'Fail',
                    'message': 'Fixture does not exist'
                }
                return make_response(jsonify(response)), 404

            fixture.update(**kwargs)
            response = {
                'status': 'success',
                'message': "Successfully updated fixture."
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update fixture.'
            }
            return make_response(jsonify(response)), 500

    @token_required
    @admin_required
    def delete(self, current_user, fixture_id):
        try:
            fixture = Fixture.find_first(id=fixture_id)
            if not fixture:
                response = {
                    'status': 'Fail',
                    'message': 'fixture does not exist'
                }
                return make_response(jsonify(response)), 404

            fixture.delete()
            response = {
                'status': 'success',
                'message': "Successfully deleted fixture."
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to delete fixture.'
            }
            return make_response(jsonify(response)), 500
