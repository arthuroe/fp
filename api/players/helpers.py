from api.models import Team


def add_jersey_to_player(players):
    for player in players:
        team = Team.find_first(id=player.get('team_id'))
        player.update({'jersey': team.jersey})
    return players
