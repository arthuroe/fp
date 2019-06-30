import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required
from api.models import FantasyLeague


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
                'message': 'No teams have been added'
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
