import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import admin_required, token_required
from api.models import GameWeek


class GameWeekView(MethodView):
    """
    View to handle Game Weeks
    """

    @token_required
    def get(self, season_id, game_week_id=None):
        if game_week_id:
            game_week = GameWeek.find_first(
                id=game_week_id, season_id=season_id)

            if not game_week_id:
                response = {
                    'status': 'fail',
                    'message': 'GameWeek does not exist'
                }
                return make_response(jsonify(response)), 404

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
                    'message': 'GameWeek does not exist'
                }
                return make_response(jsonify(response)), 404

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

    @token_required
    @admin_required
    def post(self, season_id):
        kwargs = request.json()
        kwargs.update({"season_id": season_id})

        try:
            game_week = GameWeek(**kwargs)
            game_week.save()

            response = {
                'status': 'success',
                'message': f'Successfully added {game_week.date} gameweek.'
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add gameweek.'
            }
            return make_response(jsonify(response)), 500

    @token_required
    @admin_required
    def put(self, game_week_id):
        kwargs = request.json()
        kwargs.update({"season_id": season_id, "id": game_week_id})

        try:
            game_week = GameWeek.find_first(id=game_week_id)

            if gameweek:
                game_week.update(**kwargs)

                response = {
                    'status': 'success',
                    'message': f'Successfully updated {game_week.date} gameweek.'
                }
                return make_response(jsonify(response)), 201

            response = {
                'status': 'Fail',
                'message': 'GameWeek does not exist'
            }
            return make_response(jsonify(response)), 404
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update gameweek.'
            }
            return make_response(jsonify(response)), 500

    @token_required
    @admin_required
    def delete(self, game_week_id):
        try:
            game_week = GameWeek.find_first(id=game_week_id)

            if gameweek:
                game_week.delete()

                response = {
                    'status': 'success',
                    'message': f'Successfully deleted {game_week.date} gameweek.'
                }
                return make_response(jsonify(response)), 201

            response = {
                'status': 'Fail',
                'message': 'GameWeek does not exist'
            }
            return make_response(jsonify(response)), 404
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to delete gameweek.'
            }
            return make_response(jsonify(response)), 500
