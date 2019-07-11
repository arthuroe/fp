import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from .helpers import add_jersey_to_player
from api.decorators import token_required, admin_required
from api.models import Player


class PlayersView(MethodView):
    """
    View to handle Players
    """

    @token_required
    def get(self, player_id=None):
        if player_id:
            player = Player.find_first(id=player_id)
            if not player:
                response = {
                    'status': 'fail',
                    'message': 'Player does not exist'
                }
                return make_response(jsonify(response)), 400

            player = [player.serialize()]
            add_jersey_to_player(player)
            response = {
                'status': 'success',
                'players': player
            }
            return make_response(jsonify(response)), 200

        players = Player.fetch_all()
        if not players:
            response = {
                'status': 'success',
                'message': 'No players have been added'
            }
            return make_response(jsonify(response)), 200

        players = [player.serialize() for player in players]
        add_jersey_to_player(players)
        response = {
            'status': 'success',
            'players': players
        }
        return make_response(jsonify(response)), 200

    @token_required
    @admin_required
    def post(self):
        kwargs = request.json
        team_id = request.json.get('team_id')
        name = request.json.get('name')
        position = request.json.get('position')

        if not all([name, team_id, position]):
            response = {
                'status': 'fail',
                'message': 'Incomplete data. All fields are required'
            }
            return make_response(jsonify(response)), 400

        try:
            player = Player(**kwargs)
            player.save()
            response = {
                'status': 'success',
                'message': f"Successfully added {kwargs.get('name')}"
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add player.'
            }
            return make_response(jsonify(response)), 400

    @token_required
    @admin_required
    def put(self, player_id):
        try:
            kwargs = request.json
            kwargs.update({"id": player_id})
            player = Player.find_first(id=player_id)

            if player:
                player.update(**kwargs)
                response = {
                    'status': 'Success',
                    'message': 'Updated player'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'Fail',
                'message': 'player does not exist'
            }
            return make_response(jsonify(response)), 400
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update player.'
            }
            return make_response(jsonify(response)), 400

    @token_required
    @admin_required
    def delete(self, player_id):
        try:
            player = Player.find_first(id=player_id)
            if player:
                player.delete()
                response = {
                    'status': 'Success',
                    'message': 'Deleted player'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'Fail',
                'message': 'player does not exist'
            }
            return make_response(jsonify(response)), 400
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to delete player.'
            }
            return make_response(jsonify(response)), 400
