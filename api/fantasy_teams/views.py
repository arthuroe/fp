import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from .helpers import check_max_players_from_team
from api.decorators import token_required, admin_required
from api.models import FantasyTeam, Player, User


class FantasyTeamView(MethodView):
    """
    View to handle Fantasy Teams
    """
    decorators = [token_required]

    def get(self, current_user, fantasy_team_id=None):
        if fantasy_team_id:
            fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)
            if not fantasy_team:
                response = {
                    'status': 'fail',
                    'message': 'Fantasy Team does not exist'
                }
                return make_response(jsonify(response)), 400
            response = {
                'status': 'success',
                'teams': fantasy_team.serialize()
            }
            return make_response(jsonify(response)), 200

        fantasy_teams = FantasyTeam.fetch_all()
        if not fantasy_teams:
            response = {
                'status': 'success',
                'message': 'No seasons have been added'
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'fantasy_teams': [fantasy_team.serialize() for fantasy_team in
                              fantasy_teams]
        }
        return make_response(jsonify(response)), 200

    def post(self, current_user):
        kwargs = request.json
        user_id = current_user.id
        kwargs.update({"user_id": user_id})
        name = request.json.get('name')

        if not all([name]):
            response = {
                'status': 'fail',
                'message': 'Incomplete data. All fields are required'
            }
            return make_response(jsonify(response)), 400

        try:
            user = User.find_first(id=user_id)

            if not user:
                response = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response)), 400

            fantasy_team = FantasyTeam(**kwargs)
            fantasy_team.save()

            user.fantasy_team_created = True
            user.save()

            response = {
                'status': 'success',
                'message': f'Successfully added {name}'
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add fantasy_team.'
            }
            return make_response(jsonify(response)), 400


class PlayerFantasyTeamView(MethodView):
    """
    View to handle Fantasy Team Players
    """
    decorators = [token_required]

    def get(self, current_user, fantasy_team_id):
        fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)
        players = fantasy_team.players

        if not players:
            response = {
                'status': 'success',
                'mesage': 'No players have been added'
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'players': [player.serialize() for player in players]
        }
        return make_response(jsonify(response)), 200

    def post(self, current_user, fantasy_team_id):
        player_id = request.json.get('player_id')

        try:
            fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)
            player = Player.find_first(id=player_id)

            if player in fantasy_team.players:
                response = {
                    'status': 'fail',
                    'message': 'Player already added.'
                }
                return make_response(jsonify(response)), 400
            players = fantasy_team.players

            if not check_max_players_from_team(player, fantasy_team.players):
                response = {
                    'status': 'fail',
                    'message': 'Maximum player limit from team reached.'
                }
                return make_response(jsonify(response)), 400

            if len(fantasy_team.players) >= 15:
                response = {
                    'status': 'fail',
                    'message': 'Player limit reached.'
                }
                return make_response(jsonify(response)), 400

            fantasy_team.players.append(player)
            fantasy_team.save()
            response = {
                'status': 'success',
                'message': f'Successfully added {player.name}'
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add player.'
            }
            return make_response(jsonify(response)), 400


class CaptainView(MethodView):
    """
    View to handle Fantasy Team Captains
    """
    decorators = [token_required]

    def get(self, current_user):
        fantasy_team = FantasyTeam.find_first(user_id=current_user.id)
        captain = fantasy_team.captain

        if not captain:
            response = {
                'status': 'success',
                'message': f'{fantasy_team.name} has no captain.'
            }
            return make_response(jsonify(response)), 200

        player = Player.find_first(id=captain)
        response = {
            'status': 'success',
            'player': player.serialize()
        }
        return make_response(jsonify(response)), 200

    def post(self, current_user, player_id):
        fantasy_team = FantasyTeam.find_first(user_id=current_user.id)
        player = Player.find_first(id=player_id)

        if not player:
            response = {
                'status': 'fail',
                'message': 'Player does not exist'
            }
            return make_response(jsonify(response)), 200

        try:
            fantasy_team.captain = player_id
            fantasy_team.save()
            response = {
                'status': 'success',
                'message': f'Successfully added {player.name} as captain.'
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add player as captain.'
            }
            return make_response(jsonify(response)), 400


class ViceCaptainView(MethodView):
    """
    View to handle Fantasy Team Vice Captains
    """
    decorators = [token_required]

    def get(self, current_user):
        fantasy_team = FantasyTeam.find_first(user_id=current_user.id)
        vice_captain = fantasy_team.vice_captain

        if not vice_captain:
            response = {
                'status': 'success',
                'message': f'{fantasy_team.name} has no captain.'
            }
            return make_response(jsonify(response)), 200

        player = Player.find_first(id=vice_captain)
        response = {
            'status': 'success',
            'player': player.serialize()
        }
        return make_response(jsonify(response)), 200

    def post(self, current_user, player_id):
        fantasy_team = FantasyTeam.find_first(user_id=current_user.id)
        player = Player.find_first(id=player_id)

        if not player:
            response = {
                'status': 'fail',
                'message': 'Player does not exist'
            }
            return make_response(jsonify(response)), 200

        try:
            fantasy_team.vice_captain = player_id
            fantasy_team.save()
            response = {
                'status': 'success',
                'message': (f'Successfully added {player.name} as'
                            ' vice_captain.')
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add player as vice captain.'
            }
            return make_response(jsonify(response)), 400
