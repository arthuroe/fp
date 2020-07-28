import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import admin_required, token_required
from api.models import GameWeek, Season


class GameWeekView(MethodView):
    """
    View to handle Game Weeks
    """

    @token_required
    def get(self, current_user, season_id, game_week_id=None):
        season = Season.find_first(id=season_id)
        if not season:
            response = {
                'status': 'fail',
                'message': 'Season does not exist'
            }
            return make_response(jsonify(response)), 404

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
            game_weeks = GameWeek.filter_by(season_id=season_id).all()
            if not game_weeks:
                response = {
                    'status': 'success',
                    'message': 'No game_weeks have been added'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'success',
                'gameweeks': [
                    game_week.serialize() for game_week in game_weeks]
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'gameweeks': [game_week.serialize() for game_week in game_weeks]
        }
        return make_response(jsonify(response)), 200

    @token_required
    @admin_required
    def post(self, current_user, season_id):
        kwargs = request.json
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
    def put(self, current_user, game_week_id):
        kwargs = request.json
        kwargs.update({"id": game_week_id})

        try:
            game_week = GameWeek.find_first(id=game_week_id)

            if game_week:
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
    def delete(self, current_user, game_week_id):
        try:
            game_week = GameWeek.find_first(id=game_week_id)
            if game_week:
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


class CurrentGameWeekView(MethodView):
    """
    View for current GameWeek
    """

    @token_required
    def get(self, current_user):
        current_season = Season.find_first(is_current=True)
        current_gameweek = current_season.gameweeks.filter_by(
            is_current=True).all()

        if not current_gameweek:
            response = {
                'status': 'fail',
                'message': 'GameWeek does not exist'
            }
            return make_response(jsonify(response)), 404

        fixtures = current_gameweek[0].fixtures.all()
        current_gameweek = current_gameweek[0].serialize()

        if fixtures:
            fixtures = [fixture.serialize() for fixture in fixtures]

        current_gameweek.update({"fixtures": []})
        response = {
            'status': 'success',
            'game_week': current_gameweek
        }
        return make_response(jsonify(response)), 200
