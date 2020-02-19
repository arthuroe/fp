def check_max_players_from_team(player, fantasy_team):
    teams = [player.team_id for player in fantasy_team]
    frequency = {team: teams.count(team) for team in teams}

    if player.team_id not in frequency.keys():
        return True

    for team_id in frequency:
        if team_id == player.team_id:
            return False if frequency[team_id] >= 3 else True
