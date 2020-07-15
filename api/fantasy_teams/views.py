import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from .helpers import *
from api.players.helpers import add_jersey_to_player
from api.decorators import token_required, admin_required
from api.models import FantasyTeam, Player, User, FantasyTeamPlayers


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
                return make_response(jsonify(response)), 404
            response = {
                'status': 'success',
                'teams': fantasy_team.serialize()
            }
            return make_response(jsonify(response)), 200

        fantasy_teams = FantasyTeam.fetch_all()
        if not fantasy_teams:
            response = {
                'status': 'success',
                'message': 'No Fantasy teams have been added'
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
        season_id = request.json.get('season_id')

        if not all([name, season_id]):
            response = {
                'status': 'fail',
                'message': 'Incomplete data. All fields are required'
            }
            return make_response(jsonify(response)), 400

        try:
            duplicate_fantasy_teams = FantasyTeam.find_first(name=name)

            if duplicate_fantasy_teams:
                response = {
                    'status': 'fail',
                    'message': 'Fantasy team name already exits.'
                }
                return make_response(jsonify(response)), 209

            user = User.find_first(id=user_id)

            if not user:
                response = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response)), 404

            if user.fantasy_team_created:
                response = {
                    'status': 'fail',
                    'message': f'Fantasy team already created for {user.first_name}.'
                }
                return make_response(jsonify(response)), 209

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
            return make_response(jsonify(response)), 500

    def put(self, current_user, fantasy_team_id):
        kwargs = request.json
        kwargs.update({"id": fantasy_team_id})
        name = kwargs.get('name')
        try:
            duplicate_fantasy_teams = FantasyTeam.find_first(name=name)

            if duplicate_fantasy_teams:
                response = {
                    'status': 'fail',
                    'message': 'Fantasy team name already exits.'
                }
                return make_response(jsonify(response)), 209

            fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)
            fantasy_team.update(**kwargs)
            fantasy_team.save()
            response = {
                'status': 'success',
                'message': f'Successfully updated to {fantasy_team.name}'
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update fantasy team.'
            }
            return make_response(jsonify(response)), 500


class PlayerFantasyTeamView(MethodView):
    """
    View to handle Fantasy Team Players
    """
    decorators = [token_required]

    def get(self, current_user, fantasy_team_id):
        fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)
        if not fantasy_team:
            response = {
                'status': 'fail',
                'mesage': 'fantasy_team does not exist'
            }
            return make_response(jsonify(response)), 404

        players = fantasy_team.players

        if not players:
            response = {
                'status': 'success',
                'mesage': 'No players have been added'
            }
            return make_response(jsonify(response)), 200

        starting_players = FantasyTeamPlayers.filter_by(
            fantasyteam_id=fantasy_team.id, is_sub=False).all()

        subs = FantasyTeamPlayers.filter_by(
            fantasyteam_id=fantasy_team.id, is_sub=True).all()

        starting_players = [player.serialize() for player in starting_players]
        add_player_info(starting_players)

        subs = [player.serialize() for player in subs]
        add_player_info(subs)

        response = {
            'status': 'success',
            'starting_players': starting_players,
            'subs': subs
        }
        return make_response(jsonify(response)), 200

    def post(self, current_user, fantasy_team_id):
        user_id = current_user.id
        player_id = request.json.get('player_id')

        try:
            fantasy_team = FantasyTeam.find_first(user_id=user_id)
            player = Player.find_first(id=player_id)

            if not check_current_user_is_team_owner(current_user, fantasy_team):
                response = {
                    'status': 'fail',
                    'message': "Fantasy Team doesn't belong to current user."
                }
                return make_response(jsonify(response)), 400

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

            if len(fantasy_team.players) >= 21:
                response = {
                    'status': 'fail',
                    'message': 'Player limit reached.'
                }
                return make_response(jsonify(response)), 400

            if fantasy_team.money < player.price:
                response = {
                    'status': 'fail',
                    'message': 'Not enough money to buy player'
                }
                return make_response(jsonify(response)), 400

            fantasy_team.players.append(player)
            fantasy_team.money -= player.price
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
            return make_response(jsonify(response)), 500

    def put(self, current_user, fantasy_team_id):
        player_id = request.json.get('player_id')
        current_player_id = request.json.get('current_player_id')

        try:
            fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)
            player = Player.find_first(id=player_id)
            current_player = Player.find_first(id=current_player_id)

            if not check_current_user_is_team_owner(current_user, fantasy_team):
                response = {
                    'status': 'fail',
                    'message': "Fantasy Team doesn't belong to current user."
                }
                return make_response(jsonify(response)), 400

            if player in fantasy_team.players:
                response = {
                    'status': 'fail',
                    'message': 'Player already added.'
                }
                return make_response(jsonify(response)), 400

            if (fantasy_team.money + current_player.price) < player.price:
                response = {
                    'status': 'fail',
                    'message': 'Not enough money to buy player'
                }
                return make_response(jsonify(response)), 400

            players = fantasy_team.players

            fantasy_team.players.remove(current_player)
            fantasy_team.money += current_player.price

            fantasy_team.players.append(player)
            fantasy_team.money -= player.price

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
            return make_response(jsonify(response)), 500

    def delete(self, current_user, fantasy_team_id):
        player_id = request.json.get('player_id')

        try:
            fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)
            player = Player.find_first(id=player_id)

            if not check_current_user_is_team_owner(current_user, fantasy_team):
                response = {
                    'status': 'fail',
                    'message': "Fantasy Team doesn't belong to current user."
                }
                return make_response(jsonify(response)), 400

            fantasy_team.players.remove(player)
            fantasy_team.money += player.price
            fantasy_team.save()
            response = {
                'status': 'success',
                'message': f'Successfully removed {player.name}'
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add player.'
            }
            return make_response(jsonify(response)), 500


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

    def post(self, current_user):
        fantasy_team = FantasyTeam.find_first(user_id=current_user.id)
        player_id = request.json.get('player_id')
        player = Player.find_first(id=player_id)

        if not player:
            response = {
                'status': 'fail',
                'message': 'Player does not exist'
            }
            return make_response(jsonify(response)), 404

        if player_id == fantasy_team.vice_captain:
            response = {
                'status': 'fail',
                'message': 'Player is already vice captain.'
            }
            return make_response(jsonify(response)), 400

        if player not in fantasy_team.players:
            response = {
                'status': 'fail',
                'message': 'Player not in fantasy team.'
            }
            return make_response(jsonify(response)), 400

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
            return make_response(jsonify(response)), 500


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
                'message': f'{fantasy_team.name} has no vice captain.'
            }
            return make_response(jsonify(response)), 200

        player = Player.find_first(id=vice_captain)
        response = {
            'status': 'success',
            'player': player.serialize()
        }
        return make_response(jsonify(response)), 200

    def post(self, current_user):
        fantasy_team = FantasyTeam.find_first(user_id=current_user.id)
        player_id = request.json.get('player_id')
        player = Player.find_first(id=player_id)

        if not player:
            response = {
                'status': 'fail',
                'message': 'Player does not exist'
            }
            return make_response(jsonify(response)), 404

        if player not in fantasy_team.players:
            response = {
                'status': 'fail',
                'message': 'Player not in fantasy team.'
            }
            return make_response(jsonify(response)), 400

        if player_id == fantasy_team.captain:
            response = {
                'status': 'fail',
                'message': 'Player is already captain.'
            }
            return make_response(jsonify(response)), 400

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
            return make_response(jsonify(response)), 500


class StartingPlayersView(MethodView):
    """
    View to handle Fantasy Team starting eleven
    """
    decorators = [token_required]

    def post(self, current_user):
        kwargs = request.json
        players = kwargs.get('players')

        if not current_user.fantasy_team_created:
            response = {
                'status': 'fail',
                'message': 'Please first create a fantasy_team'
            }
            return make_response(jsonify(response)), 400

        try:
            fantasy_team = FantasyTeam.find_first(user_id=current_user.id)

            if not fantasy_team.players:
                response = {
                    'status': 'fail',
                    'message': 'No players added to fantasy team.'
                }
                return make_response(jsonify(response)), 400

            for player in players:
                fantasy_team_player = FantasyTeamPlayers.find_first(
                    fantasyteam_id=fantasy_team.id, player_id=player.get('id'))

                if not fantasy_team_player:
                    logging.error(f"Player not in Fantasy Team")
                    continue

                fantasy_team_player.is_captain = player.get('is_captain', False)
                fantasy_team_player.is_vice_captain = player.get(
                    'is_vice_captain', False)
                fantasy_team_player.is_sub = player.get('is_sub', False)
                fantasy_team_player.save()

            response = {
                'status': 'success',
                'message': 'Saved fantasy team.'
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to submit players.'
            }
            return make_response(jsonify(response)), 500

    def put(self, current_user):
        kwargs = request.json
        player_to_start = kwargs.get('player_to_start')
        player_to_sub = kwargs.get('player_to_sub')

        if not all([player_to_start, player_to_sub]):
            response = {
                'status': 'fail',
                'message': 'Provide player to substitute and substitute'
            }
            return make_response(jsonify(response)), 400

        try:
            fantasy_team = FantasyTeam.find_first(user_id=current_user.id)
            player_to_start = FantasyTeamPlayers.find_first(
                fantasyteam_id=fantasy_team.id, player_id=player_to_start)
            player_to_start.is_sub = False
            player_to_start.save()

            player_to_sub = FantasyTeamPlayers.find_first(
                fantasyteam_id=fantasy_team.id, player_id=player_to_sub)
            player_to_sub.is_sub = True
            player_to_sub.save()

            response = {
                'status': 'success',
                'message': 'Successfully substituted player.'
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to substitute player.'
            }
            return make_response(jsonify(response)), 500


class AddMultiplePlayerView(MethodView):
    """
    View to handle adding multiple players at once to team
    """
    decorators = [token_required]

    def post(self, current_user):
        """
        TODO: clean up this later.
        Look at checking the current implementation of checking team owner
        before making any modifications
        """
        user_id = current_user.id
        players = request.json.get('players')

        try:
            fantasy_team = FantasyTeam.find_first(user_id=user_id)

            for player in players:
                player = Player.find_first(id=player.get('id'))

                if player in fantasy_team.players:
                    response = {
                        'status': 'fail',
                        'message': f'Player {player.name} already added.'
                    }
                    return make_response(jsonify(response)), 400

                if not check_max_players_from_team(player, fantasy_team.players):
                    response = {
                        'status': 'fail',
                        'message': 'Maximum player limit from team reached.'
                    }
                    return make_response(jsonify(response)), 400

                if len(fantasy_team.players) >= 21:
                    response = {
                        'status': 'fail',
                        'message': 'Player limit reached.'
                    }
                    return make_response(jsonify(response)), 400

                if fantasy_team.money < player.price:
                    response = {
                        'status': 'fail',
                        'message': 'Not enough money to buy player'
                    }
                    return make_response(jsonify(response)), 400

                fantasy_team.players.append(player)
                fantasy_team.money -= player.price
            fantasy_team.save()
            response = {
                'status': 'success',
                'message': f'Successfully added players'
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add players.'
            }
            return make_response(jsonify(response)), 500
