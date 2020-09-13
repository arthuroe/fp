from api.models import FantasyTeam


def get_fantasy_team_info(league_teams):
    teams = []
    for team in league_teams:
        details = FantasyTeam.find_first(id=team.fantasyteam_id)
        team = team.serialize()
        team.update(details.serialize())
        teams.append(team)
    return teams
