import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required
from api.models import FantasyLeague, FantasyTeam


class FantasyLeagueView(MethodView):
    """ View to handle Fantasy Leagues """

    def get(self, league_id=None):
        if league_id:
            league = FantasyLeague.find_first(id=league_id)
            if not league:
                response = {
                    'status': 'fail',
                    'message': 'League does not exist'
                }
                return make_response(jsonify(response)), 400
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

    def post(self):
        post_data = request.json
        name = post_data.get('name')

        if not all([name]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. All fields are required')
            }
            return make_response(jsonify(response)), 400

        try:
            fantasy_league = FantasyLeague(name=name)
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
            return make_response(jsonify(response)), 400


class FantasyLeagueUsersView(MethodView):

    def get(self):
        pass

    def post(self):
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
                return make_response(jsonify(response)), 400

            if fantasy_team in fantasy_team.players:
                response = {
                    'status': 'fail',
                    'message': 'Team already added to league.'
                }
                return make_response(jsonify(response)), 400

            fantasy_league.fantasy_teams.append(fantasy_team)
            fantasy_league.save()
            response = {
                    'status': 'Success',
                    'message': 'Team already added to league.'
                }
            return make_response(jsonify(response)), 400

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'Success',
                'message': f'Successfully added {fantasy_team.name} to {fantasy_league.name}.'
            }
            return make_response(jsonify(response)), 400
