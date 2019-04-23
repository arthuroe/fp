import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required, admin_required
from api.models import Team


class TeamsView(MethodView):
    """
    View to handle Teams
    """

    def post(self):
        post_data = request.json
        name = post_data.get('name')
        manager = post_data.get('manager')

        if not all([name, manager]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. All fields are required')
            }
            return make_response(jsonify(response)), 400

        try:
            team = Team(name=name, manager=manager)
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
                'message': 'Failed to add flight.'
            }
            return make_response(jsonify(response)), 400

    def get(self):
        teams = Team.fetch_all()
        import pdb
        pdb.set_trace()
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
