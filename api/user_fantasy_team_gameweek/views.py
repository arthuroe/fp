import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.auth.helpers import *
from api.decorators import token_required
from api.gameweek_stats.helpers import get_fantasy_player_stats
from api.models import UserFantasyTeamGameWeek, GameWeek, FantasyTeam


class UserFantasyTeamGameWeekView(MethodView):
    """
    View to enable users view and update their details
    """
    decorators = [token_required]

    def get(self, current_user, game_week_id):
        user_id = current_user.id
        game_week = GameWeek.find_first(id=game_week_id)
        if not game_week:
            response = {
            'status': 'fail',
            'message': 'User fantasy gameweek does not exist.',
            }
            return make_response(jsonify(response)), 400

        user_fantasy_team_gameweek = UserFantasyTeamGameWeek.find_first(user_id=user_id, game_week_id=game_week_id)
        fantasy_team_id = current_user.fantasy_team.all()[0].id

        if user_fantasy_team_gameweek:
            fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)
            fantasy_team_player_stats, points = get_fantasy_player_stats(
            fantasy_team, game_week_id)
            actual_points = points - user_fantasy_team_gameweek.points_deductible
            user_fantasy_team_gameweek.update(points=actual_points, game_week_points=points, id=user_fantasy_team_gameweek.id)
            user_fantasy_team_gameweek.save()
            response = {
            'status': 'Success',
            'game_weekInfo': user_fantasy_team_gameweek.serialize(),
            }
            return make_response(jsonify(response)), 200       

        user_fantasy_team_gameweek = UserFantasyTeamGameWeek(fantasy_team_id=fantasy_team_id, game_week_id=game_week_id, user_id=user_id)
        user_fantasy_team_gameweek.save()

        response = {
        'status': 'Success',
        'game_weekInfo': user_fantasy_team_gameweek.serialize(),
        }
        return make_response(jsonify(response)), 200    

    def post(self, current_user, game_week_id):
        kwargs = request.json
        game_week_id = kwargs.get('game_week_id')
        points_deductible = kwargs.get('points_deductible', 0)
        user_id = current_user.id
        fantasy_team_id = current_user.fantasy_team.all()[0].id
        kwargs.update({"user_id": user_id, "fantasy_team_id": fantasy_team_id})
    
        try:
            game_week = GameWeek.find_first(id=game_week_id)
            if not game_week:
                response = {
                'status': 'fail',
                'message': 'User fantasy gameweek does not exist.',
                }
                return make_response(jsonify(response)), 400
            
            user_fantasy_team_gameweek = UserFantasyTeamGameWeek.find_first(user_id=user_id, game_week_id=game_week_id)

            fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)
            if not fantasy_team or not fantasy_team.players:
                response = {
                    'status': 'fail',
                    'message': 'FantasyTeam does not exist or does not have players.'
                }
                return make_response(jsonify(response)), 404

            fantasy_team_player_stats, points = get_fantasy_player_stats(
            fantasy_team, game_week_id)
            kwargs.update({"points": (points - points_deductible), "game_week_points": points, "id": user_fantasy_team_gameweek.id})

            if user_fantasy_team_gameweek:

                user_fantasy_team_gameweek.update(**kwargs)
                user_fantasy_team_gameweek.save()
                response = {
                    'status': 'success',
                    'message': f'Successfully updated user fantasy gameweek.'
                }
                return make_response(jsonify(response)), 201

            user_fantasy_team_gameweek = UserFantasyTeamGameWeek(**kwargs)
            user_fantasy_team_gameweek.save()
            response = {
                    'status': 'success',
                    'message': f'Successfully added user fantasy gameweek.'
                }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add user fantasy gameweek. Please try again.'
            }
            return make_response(jsonify(response)), 500
