import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required, admin_required
from api.models import Season, Team


class TeamsView(MethodView):
    """
    View to handle Teams
    """

    @token_required
    @admin_required
    def post(self, current_user):
        post_data = request.json
        name = post_data.get('name')
        manager = post_data.get('manager')
        logo = post_data.get("logo")
        season_id = post_data.get('season_id')

        if not all([name, manager, season_id]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. All fields are required')
            }
            return make_response(jsonify(response)), 400

        try:
            season = Season.find_first(id=season_id)
            team = Team(name=name, manager=manager, logo=logo)
            season.teams.append(team)
            season.save()
            team.save()
            response = {
                'status': 'success',
                'message': f'Successfully added {name}'
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add team.'
            }
            return make_response(jsonify(response)), 500

    def get(self, team_id=None):
        if team_id:
            team = Team.find_first(id=team_id)
            if not team:
                response = {
                    'status': 'fail',
                    'message': 'Team does not exist'
                }
                return make_response(jsonify(response)), 404
            response = {
                'status': 'success',
                'team': team.serialize()
            }
            return make_response(jsonify(response)), 200

        teams = Team.fetch_all()
        if not teams:
            response = {
                'status': 'success',
                'message': 'No teams have been added'
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'teams': [team.serialize() for team in teams]
        }
        return make_response(jsonify(response)), 200

    @token_required
    @admin_required
    def put(self, current_user, team_id):
        try:
            kwargs = request.json
            kwargs.update({"id": team_id})
            team = Team.find_first(id=team_id)

            if team:
                team.update(**kwargs)
                response = {
                    'status': 'Success',
                    'message': 'Updated team'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'Fail',
                'message': 'Team does not exist'
            }
            return make_response(jsonify(response)), 404
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update team.'
            }
            return make_response(jsonify(response)), 500

    @token_required
    @admin_required
    def delete(self, current_user, team_id):
        try:
            team = Team.find_first(id=team_id)
            if team:
                team.delete()
                response = {
                    'status': 'Success',
                    'message': 'Deleted Team'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'Fail',
                'message': 'Team does not exist'
            }
            return make_response(jsonify(response)), 404
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to delete team.'
            }
            return make_response(jsonify(response)), 500


class LeagueStandingsView(MethodView):
    """
    View to handle league standings
    """

    def get(self, season_id):
        season = Season.find_first(id=season_id)
        if not season:
            response = {
                'status': 'fail',
                'message': 'Season does not exist'
            }
            return make_response(jsonify(response)), 404

        teams = season.teams.order_by(Team.league_position.asc()).all()
        response = {
            'status': 'success',
            'teams': [team.serialize() for team in teams]
        }
        return make_response(jsonify(response)), 200
