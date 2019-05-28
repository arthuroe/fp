import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required, admin_required
from api.models import Season


class SeasonsView(MethodView):
    """
    View to handle Teams
    """

    def get(self, season_id=None):
        seasons = Season.fetch_all()
        if not seasons:
            response = {
                'status': 'success',
                'message': 'No seasons have been added'

            }
            return make_response(jsonify(response)), 200

        if season_id:
            seasons = Season.find_first(id=season_id)
            response = {
                'status': 'success',
                'teams': [season.serialize() for season in seasons]
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'teams': [season.serialize() for season in seasons]
        }
        return make_response(jsonify(response)), 200
