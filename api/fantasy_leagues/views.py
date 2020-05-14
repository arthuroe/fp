import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required
from api.models import FantasyLeague, FantasyTeam, FantasyLeagueTeam


class FantasyLeagueView(MethodView):
    """ View to handle Fantasy Leagues """
    decorators = [token_required]

    def get(self, current_user, league_id=None):
        if league_id:
            league = FantasyLeague.find_first(id=league_id)
            if not league:
                response = {
                    'status': 'fail',
                    'message': 'League does not exist'
                }
                return make_response(jsonify(response)), 404
            response = {
                'status': 'success',
                'league': league.serialize()
            }
            return make_response(jsonify(response)), 200

        leagues = FantasyLeague.fetch_all()
        if not leagues:
            response = {
                'status': 'success',
                'message': 'No leagues have been added'
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'leagues': [league.serialize() for league in leagues]
        }
        return make_response(jsonify(response)), 200

    def post(self, current_user):
        post_data = request.json
        name = post_data.get('name')

        if not all([name]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. All fields are required')
            }
            return make_response(jsonify(response)), 400

        try:
            fantasy_league = FantasyLeague(**post_data)
            fantasy_league.save()
            response = {
                'status': 'success',
                'message': f'Successfully added {name}'
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add league.'
            }
            return make_response(jsonify(response)), 500


class FantasyLeagueUsersView(MethodView):
    """View to handle Fantasy League for users"""
    decorators = [token_required]

    def get(self, current_user, fantasy_league_id):
        league = FantasyLeague.find_first(id=fantasy_league_id)
        if not league:
            response = {
                'status': 'fail',
                'message': 'League does not exist'
            }
            return make_response(jsonify(response)), 404

        league_teams = FantasyLeagueTeam.filter_by(
            fantasyleague_id=fantasy_league_id).order_by(
                FantasyLeagueTeam.points.desc())

        response = {
            'status': 'success',
            'league_teams': [team.serialize() for team in league_teams]
        }
        return make_response(jsonify(response)), 200

    def post(self, current_user):
        fantasy_team_id = request.json.get('fantasy_team_id')
        fantasy_league_id = request.json.get('fantasy_league_id')

        try:
            fantasy_league = FantasyLeague.find_first(id=fantasy_league_id)
            fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)

            if not fantasy_team or not fantasy_league:
                response = {
                    'status': 'fail',
                    'message': 'Team or league does not exist.'
                }
                return make_response(jsonify(response)), 404

            if fantasy_team in fantasy_league.fantasy_teams:
                response = {
                    'status': 'fail',
                    'message': 'Team already added to league.'
                }
                return make_response(jsonify(response)), 400

            fantasy_league.fantasy_teams.append(fantasy_team)
            fantasy_league.save()
            response = {
                'status': 'Success',
                'message': (f'Successfully added {fantasy_team.name}'
                            f' to {fantasy_league.name}.')
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': f'Error adding team to league.'
            }
            return make_response(jsonify(response)), 500

    def delete(self, current_user):
        fantasy_team_id = request.json.get('fantasy_team_id')
        fantasy_league_id = request.json.get('fantasy_league_id')

        try:
            fantasy_league = FantasyLeague.find_first(id=fantasy_league_id)
            fantasy_team = FantasyTeam.find_first(id=fantasy_team_id)

            if not fantasy_team or not fantasy_league:
                response = {
                    'status': 'fail',
                    'message': 'Team or league does not exist.'
                }
                return make_response(jsonify(response)), 404

            if fantasy_team not in fantasy_league.fantasy_teams:
                response = {
                    'status': 'fail',
                    'message': 'Team already not in league.'
                }
                return make_response(jsonify(response)), 400

            fantasy_league.fantasy_teams.remove(fantasy_team)
            fantasy_league.save()
            response = {
                'status': 'Success',
                'message': (f'{fantasy_team.name} removed from'
                            f' {fantasy_league.name}.')
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': f'Error removing team from league.'
            }
            return make_response(jsonify(response)), 500
