import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from .helpers import award_points
from api.decorators import admin_required, token_required
from api.models import PlayerGameWeek


class GameWeekStatsView(MethodView):
    """
    View to handle GameWeek stats
    """

    @token_required
    def get(self, current_user, game_week_id, player_id=None):
        gameweek = GameWeek.find_first(id=game_week_id)
        if not game_week:
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

    @token_required
    @admin_required
    def post(self, current_user, game_week_id, player_id):
        kwargs = request.json
        kwargs.update({"game_week_id": game_week_id, "player_id": player_id})

        try:
            check_gameweek_stats_exist = PlayerGameWeek.filter_by(
                player_id=player_id, game_week_id=game_week_id).all()

            if check_gameweek_stats_exist:
                response = {
                    'status': 'fail',
                    'Message': 'Stats already added, please update exsiting stats.'
                }
                return make_response(jsonify(response)), 400

            gameweek_stats = PlayerGameWeek(**kwargs)
            gameweek_stats.gameweek_points = award_points(**kwargs)
            gameweek_stats.save()
            response = {
                'status': 'success',
                'stats': gameweek_stats.serialize()
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add gameweek stats.'
            }
            return make_response(jsonify(response)), 500

    @token_required
    @admin_required
    def put(self, current_user, game_week_id, player_id):
        kwargs = request.json
        kwargs.update({"game_week_id": game_week_id, "player_id": player_id})

        try:
            stats = PlayerGameWeek.filter_by(
                player_id=player_id, game_week_id=game_week_id).all()[0]

            stat_id = stats.id
            stat = PlayerGameWeek.find_first(id=stat_id)
            stat.update(**kwargs)
            stat.gameweek_points = award_points(**kwargs)
            response = {
                'status': 'success',
                'stats': stat.serialize()
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update gameweek stats.'
            }
            return make_response(jsonify(response)), 500

    @token_required
    @admin_required
    def delete(self):
        pass
