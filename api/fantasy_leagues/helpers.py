from flask import make_response, jsonify
from api.models import FantasyTeam


def get_fantasy_team_info(league_teams):
    teams = []
    for team in league_teams:
        details = FantasyTeam.find_first(id=team.fantasyteam_id)
        team = team.serialize()
        team.update(details.serialize())
        teams.append(team)
    return teams


def get_current_user_fantasy_team(current_user):
    fantasy_team = current_user.fantasy_team.all()
    if not fantasy_team:
        response = {
            'status': 'fail',
            'message': 'User has not created fantasy team.'
        }
        return make_response(jsonify(response)), 400

    return current_user.fantasy_team.all()[0].id
