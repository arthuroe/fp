import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import admin_required, token_required
from api.models import PlayerGameWeek


class GameWeekStatsView(MethodView):
    """
    View to handle GameWeek stats
    """

    def get(self, current_user, game_week_id, player_id=None):
        if not game_week_id:
            response = {
                'status': 'fail',
                'message': 'GameWeek does not exist'
            }
            return make_response(jsonify(response)), 404

        if player_id:
            player_stats = PlayerGameWeek.filter_by(
                game_week_id=game_week_id, player_id=player_id).all()
            response = {
                'status': 'success',
                'gameweek_stats': [stat.serialize() for stat in player_stats]
            }
            return make_response(jsonify(response)), 200

        player_stats = PlayerGameWeek.filter_by(
            game_week_id=game_week_id).all()
        response = {
            'status': 'success',
            'gameweek_stats': [stat.serialize() for stat in player_stats]
        }
        return make_response(jsonify(response)), 200

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
