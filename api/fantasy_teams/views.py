import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required, admin_required
from api.models import FantasyTeam


class FantasyTeamView(MethodView):
    """
    View to Fantasy Teams
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
            fantasy_team = FantasyTeam(**kwargs)
            fantasy_team.save()
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
