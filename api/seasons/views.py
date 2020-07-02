import logging

from flask import request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required, admin_required
from api.models import Season


class SeasonsView(MethodView):
    """
    View to handle Seasons
    """

    @token_required
    @admin_required
    def get(self, current_user, season_id=None):
        if season_id:
            season = Season.find_first(id=season_id)
            if not season:
                response = {
                    'status': 'fail',
                    'message': 'Season does not exist'
                }
                return make_response(jsonify(response)), 404
            response = {
                'status': 'success',
                'season': season.serialize()
            }
            return make_response(jsonify(response)), 200

        seasons = Season.fetch_all()
        if not seasons:
            response = {
                'status': 'success',
                'message': 'No seasons have been added'
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'seasons': [season.serialize() for season in seasons]
        }
        return make_response(jsonify(response)), 200

    @token_required
    @admin_required
    def post(self, current_user):
        post_data = request.json
        logo = post_data.get('logo')
        name = post_data.get('name')
        start_date = post_data.get('start_date')
        end_date = post_data.get('end_date')

        if not all([name, start_date, end_date]):
            response = {
                'status': 'fail',
                'message': 'Incomplete data. All fields are required'
            }
            return make_response(jsonify(response)), 400

        try:
            if Season.filter_by(start_date=start_date, end_date=end_date).all():
                return make_response(
                    jsonify(
                        {
                            'status': 'fail',
                            'message': 'Season already created'
                        }
                    ), 409
                )

            season = Season(name=name, start_date=start_date,
                            end_date=end_date, logo=logo)
            season.save()
            response = {
                'status': 'success',
                'message': f'Successfully added {name}'
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add season.'
            }
            return make_response(jsonify(response)), 500

    @token_required
    @admin_required
    def put(self, current_user, season_id):
        try:
            kwargs = request.json
            kwargs.update({"id": season_id})
            season = Season.find_first(id=season_id)

            if season:
                season.update(**kwargs)
                response = {
                    'status': 'Success',
                    'message': 'Updated season'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'Fail',
                'message': 'Season does not exist'
            }
            return make_response(jsonify(response)), 404
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update season.'
            }
            return make_response(jsonify(response)), 500

    @token_required
    @admin_required
    def delete(self, current_user, season_id):
        try:

            season = Season.find_first(id=season_id)
            if season:
                season.delete()
                response = {
                    'status': 'Success',
                    'message': 'Deleted season'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'Fail',
                'message': 'Season does not exist'
            }
            return make_response(jsonify(response)), 404
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to delete season.'
            }
            return make_response(jsonify(response)), 500


class CurrentSeasonView(MethodView):
    """
    View to handle current season
    """

    def get(self):
        season = Season.find_first(is_current=True)
        if not season:
            response = {
                'status': 'success',
                'message': 'No season marked as current yet.'
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'season': season.serialize()
        }
        return make_response(jsonify(response)), 200
