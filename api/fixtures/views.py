import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from .helpers import *
from api.decorators import admin_required, token_required
from api.models import Fixture, GameWeek


class FixturesView(MethodView):
    """
    View to handle Fixturess
    """

    @token_required
    def get(self, current_user, game_week_id=None, fixture_id=None):
        if game_week_id:
            game_week = GameWeek.find_first(id=game_week_id)
            if not game_week:
                response = {
                    'status': 'fail',
                    'message': 'GameWeek does not exist'
                }
                return make_response(jsonify(response)), 404

            fixtures = Fixture.filter_by(game_week_id=game_week_id)

            response = {
                'status': 'success',
                'fixtures': [fixture.serialize() for fixture in fixtures.all()]
            }
            return make_response(jsonify(response)), 200

        if fixture_id:
            fixture = Fixture.find_first(id=fixture_id)
            if not fixture:
                response = {
                    'status': 'fail',
                    'message': 'GameWeek does not exist'
                }
                return make_response(jsonify(response)), 404

            stats = fixture.player_stats.filter_by(
                game_week_id=fixture.game_week_id).all()

            serialized_fixture = fixture.serialize()
            home_team, away_team = get_player_stats(stats, fixture)

            serialized_fixture.update(
                {
                    "player_stats": {
                        "home_team": home_team, "away_team": away_team
                    }
                }
            )

            response = {
                'status': 'success',
                'fixture': serialized_fixture
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
    def post(self, current_user):
        kwargs = request.json
        game_week_id = kwargs.get('game_week_id')
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
        kwargs = request.json
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
