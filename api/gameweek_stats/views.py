import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api import app
from .helpers import *
from api.decorators import admin_required, token_required
from api.models import PlayerGameWeek, GameWeek, FantasyTeam, Player, FantasyTeamPlayerGameWeek, Season


class GameWeekStatsView(MethodView):
    """
    View to handle GameWeek stats
    """

    @token_required
    def get(self, current_user, game_week_id, player_id=None):
        game_week = GameWeek.find_first(id=game_week_id)
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
        print("Player stats being added", kwargs)

        try:
            check_gameweek_stats_exist = PlayerGameWeek.filter_by(
                player_id=player_id, game_week_id=game_week_id).all()

            if check_gameweek_stats_exist:
                response = {
                    'status': 'fail',
                    'Message': (
                        'Stats already added, please update exsiting stats.')
                }
                return make_response(jsonify(response)), 400

            gameweek_stats = PlayerGameWeek(**kwargs)
            gameweek_stats.gameweek_points = award_points(**kwargs)
            gameweek_stats.save()

            player = Player.find_first(id=player_id)

            update_fantasy_player_gameweek(player, gameweek_stats)

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
        print("Player stats being added", kwargs)
        
        try:
            stats = PlayerGameWeek.filter_by(
                player_id=player_id, game_week_id=game_week_id).all()[0]

            stat_id = stats.id
            stat = PlayerGameWeek.find_first(id=stat_id)
            kwargs.update({"id": stat_id})
            stat.update(**kwargs)
            stat.gameweek_points = award_points(**kwargs)
            stat.save()

            player = Player.find_first(id=player_id)

            update_fantasy_player_gameweek(player, stat)
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
    def delete(self, current_user, game_week_id, player_id):
        try:
            stats = PlayerGameWeek.filter_by(
                player_id=player_id, game_week_id=game_week_id).all()[0]

            stat_id = stats.id
            stat = PlayerGameWeek.find_first(id=stat_id)
            stat.delete()
            response = {
                'status': 'success',
                'message': 'Successfully deleted player stats'
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to delete gameweek stats.'
            }
            return make_response(jsonify(response)), 500


class GameWeekStatsFantasyView(MethodView):
    """
    View to handle GameWeek fantasy team stats
    """

    @token_required
    def get(self, current_user, game_week_id, fantasy_team_id):
        game_week = GameWeek.find_first(id=game_week_id)
        if not game_week:
            response = {
                'status': 'fail',
                'message': 'GameWeek does not exist'
            }
            return make_response(jsonify(response)), 404

        fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)

        if not fantasy_team or not fantasy_team.players:
            response = {
                'status': 'fail',
                'message': 'FantasyTeam does not exist or does not have players.'
            }
            return make_response(jsonify(response)), 404

        fantasy_team_player_stats, points = get_fantasy_player_stats(
            fantasy_team, game_week_id)

        response = {
            'status': 'success',
            'fantasy_team_stats': fantasy_team_player_stats,
            "total_points": points
        }
        return make_response(jsonify(response)), 200

    @token_required
    def post(self, current_user, game_week_id):
        gameweek = GameWeek.find_first(id=game_week_id)
        if not gameweek:
            response = {
                'status': 'fail',
                'message': 'GameWeek does not exist'
            }
            return make_response(jsonify(response)), 404
            
        fixtures = gameweek.fixtures.all()

        add_initial_player_stats(app, fixtures)

        response = {
            'status': 'success',
            'message': 'Stats are being update please wait.'
        }
        return make_response(jsonify(response)), 200


class TeamOfWeekView(MethodView):
    "View to handle team of the week"
    decorators = [token_required]

    def get(self, current_user, game_week_id):
        game_week = GameWeek.find_first(id=game_week_id)
        if not game_week:
            response = {
                'status': 'fail',
                'message': 'GameWeek does not exist'
            }
            return make_response(jsonify(response)), 404

        players = PlayerGameWeek.filter_by(game_week_id=game_week_id)

        team_of_the_week = []

        if players:
            team_of_the_week.extend(
                get_top_players_in_category(players, 'FR', 3))
            team_of_the_week.extend(
                get_top_players_in_category(players, 'SR', 2))
            team_of_the_week.extend(
                get_top_players_in_category(players, 'BR', 3))
            team_of_the_week.extend(
                get_top_players_in_category(players, 'HB', 2))
            team_of_the_week.extend(
                get_top_players_in_category(players, 'C', 2))
            team_of_the_week.extend(
                get_top_players_in_category(players, 'WB', 3))

        if team_of_the_week:
            team = []
            for player_stats in team_of_the_week:
                info = player_stats.player_info
                player_stats = player_stats.serialize()
                player_info = info.serialize()
                player_info['jersey'] = info.team.jersey
                player_info['player_stats'] = player_stats
                team.append(player_info)
            team_of_the_week = team

            response = {
                'status': 'success',
                'team': team_of_the_week
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'team': 'No stats have been provided for this yet'
        }
        return make_response(jsonify(response)), 200
