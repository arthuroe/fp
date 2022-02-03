import logging
from api.models.season import Season

from flask import request, make_response, jsonify
from flask.views import MethodView

from .helpers import *
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
        user_id = current_user.id
        code = generate_league_code()
        post_data.update({'code': code})

        if not all([name]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. All fields are required')
            }
            return make_response(jsonify(response)), 400

        try:
            existing_league = FantasyLeague.find_first(name=name)
            if existing_league:
                response = {
                    'status': 'fail',
                    'message': 'Fantasy league name already exists.'
                }
                return make_response(jsonify(response)), 400

            fantasy_league = FantasyLeague(**post_data)
            fantasy_league.save()

            user_fantasy_team = FantasyTeam.find_first(user_id=user_id)
            fantasy_league.fantasy_teams.append(user_fantasy_team)
            fantasy_league.save()

            response = {
                'status': 'success',
                'message': f'Successfully added {name}',
                'code': code
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

    def get(self, current_user, fantasy_league_id=None):
        user_id = current_user.id
        if fantasy_league_id:
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

            all_teams = get_fantasy_team_info(league_teams)
            sorted_teams = sorted(
                all_teams, key=lambda i: i['points'], reverse=True)
            response = {
                'status': 'success',
                'league_teams': sorted_teams
            }
            return make_response(jsonify(response)), 200

        user_fantasy_leagues = FantasyLeague.query.join(
            FantasyTeam, FantasyLeague.fantasy_teams
        ).filter(FantasyTeam.user_id == user_id).all()

        response = {
            'status': 'success',
            'leagues': [league.serialize() for league in user_fantasy_leagues]
        }
        return make_response(jsonify(response)), 200

    def post(self, current_user):
        try:
            fantasy_team_id = get_current_user_fantasy_team(current_user)
            fantasy_league_id = request.json.get('fantasy_league_id')

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
                'message': (f'Successfully joined {fantasy_team.name}'
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
        fantasy_team_id = get_current_user_fantasy_team(current_user)
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
                'message': f'{fantasy_team.name} left {fantasy_league.name}.'
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': f'Error removing team from league.'
            }
            return make_response(jsonify(response)), 500


class GlobalFanstayLeagueView(MethodView):
    """View to handle Fantasy League for users"""
    decorators = [token_required]

    def get(self, current_user):
        user_id = current_user.id

        current_season = Season.find_first(is_current=True)
        fantasy_teams = FantasyTeam.filter_by(season_id=current_season.id)

        all_teams = get_global_fantasy_team_info(fantasy_teams)
        sorted_teams = sorted(
            all_teams, key=lambda i: i['points'], reverse=True)
        response = {
            'status': 'success',
            'all_teams': sorted_teams
        }
        return make_response(jsonify(response)), 200
