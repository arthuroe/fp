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
        logo = post_data.get("logo")

        if not all([name, manager]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. All fields are required')
            }
            return make_response(jsonify(response)), 400

        try:
            team = Team(name=name, manager=manager, logo=logo)
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
            return make_response(jsonify(response)), 400

    def get(self):
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

    def put(self, team_id):
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
            return make_response(jsonify(response)), 400
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update team.'
            }
            return make_response(jsonify(response)), 400

    def delete(self, team_id):
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
            return make_response(jsonify(response)), 400
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to delete team.'
            }
            return make_response(jsonify(response)), 400
