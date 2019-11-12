import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required
from api.models import GameWeek


class GameWeekView(MethodView):
    """
    View to handle Game Weeks
    """

    def get(self, season_id, game_week_id=None):
        if game_week_id:
            game_week = GameWeek.find_first(
                id=game_week_id, season_id=season_id)

            if not game_week_id:
                response = {
                    'status': 'fail',
                    'message': 'GameWeek does not exist'
                }
                return make_response(jsonify(response)), 400

            response = {
                'status': 'success',
                'game_week': game_week.serialize()
            }
            return make_response(jsonify(response)), 200

        if season_id and not game_week_id:
            game_weeks = GameWeek.filter_by(season_id=season_id)
            if not season_id:
                response = {
                    'status': 'fail',
                    'message': 'Season does not exist'
                }
                return make_response(jsonify(response)), 400

            response = {
                'status': 'success',
                'gameweeks': [
                    game_week.serialize() for game_week in game_weeks]
            }
            return make_response(jsonify(response)), 200

        game_weeks = GameWeek.fetch_all()
        if not game_weeks:
            response = {
                'status': 'success',
                'message': 'No game_weeks have been added'
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'gameweeks': [game_week.serialize() for game_week in game_weeks]
        }
        return make_response(jsonify(response)), 200

    def post(self, season_id):
        pass
