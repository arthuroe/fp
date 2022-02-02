from flask import make_response, jsonify
from api.models import GameWeek, FantasyTeam, UserFantasyTeamGameWeek, fantasy_team
from sqlalchemy.sql import func


def get_fantasy_team_info(league_teams):
    teams = []
    current_gameweek = GameWeek.find_first(is_current=True)
    for team in league_teams:
        fantasy_team_id = team.fantasyteam_id
        team_sum = UserFantasyTeamGameWeek.query.with_entities(
            func.sum(UserFantasyTeamGameWeek.points).label('sum')
        ).filter(
            UserFantasyTeamGameWeek.fantasy_team_id == team.fantasyteam_id
        ).all()

        details = FantasyTeam.find_first(id=team.fantasyteam_id)

        team = team.serialize()
        team.update(details.serialize())

        if team_sum and team_sum[0][0]:
            team['points'] = team_sum[0][0]

        current_gameweek_points = get_current_gameweek_points(
            fantasy_team_id, current_gameweek.id)
        team['current_gameweek_points'] = current_gameweek_points
        teams.append(team)

    return teams


def get_global_fantasy_team_info(all_teams):
    teams = []
    current_gameweek = GameWeek.find_first(is_current=True)
    for team in all_teams:
        team_sum = UserFantasyTeamGameWeek.query.with_entities(
            func.sum(UserFantasyTeamGameWeek.points).label('sum')
        ).filter(
            UserFantasyTeamGameWeek.fantasy_team_id == team.id
        ).all()

        current_gameweek_points = get_current_gameweek_points(
            team.id, current_gameweek.id)
        team = team.serialize()
        team['current_gameweek_points'] = current_gameweek_points
        team['points'] = 0
        if team_sum and team_sum[0][0]:
            team['points'] = team_sum[0][0]
        teams.append(team)

    return teams


def get_current_gameweek_points(fantasy_team_id, current_gameweek_id):
    user_fantasy_team_gameweek = UserFantasyTeamGameWeek.filter_by(
        fantasy_team_id=fantasy_team_id, game_week_id=current_gameweek_id).all()
    if user_fantasy_team_gameweek:
        return user_fantasy_team_gameweek[0].points
    return 0


def get_current_user_fantasy_team(current_user):
    fantasy_team = current_user.fantasy_team.all()
    if not fantasy_team:
        response = {
            'status': 'fail',
            'message': 'User has not created fantasy team.'
        }
        return make_response(jsonify(response)), 400

    return current_user.fantasy_team.all()[0].id
