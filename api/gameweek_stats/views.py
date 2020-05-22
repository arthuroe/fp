import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import admin_required, token_required


class GameWeekStatsView(MethodView):
    """
    View to handle GameWeek stats
    """

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
