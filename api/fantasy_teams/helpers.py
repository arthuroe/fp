from api.models import Player


def check_max_players_from_team(player, fantasy_team):
    teams = [player.team_id for player in fantasy_team]
    frequency = {team: teams.count(team) for team in teams}

    if player.team_id not in frequency.keys():
        return True

    for team_id in frequency:
        if team_id == player.team_id:
            return False if frequency[team_id] >= 3 else True


def add_player_info(fantasy_players):
    for fantasy_player in fantasy_players:
        player = Player.find_first(id=fantasy_player.get('player_id'))
        jersey = player.team.jersey
        player = player.serialize()
        del player["id"]
        del player["uuid"]
        fantasy_player.update(player)
        fantasy_player.update({"jersey": jersey})
    return fantasy_players
