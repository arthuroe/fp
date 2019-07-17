def check_max_players_from_team(player, fantasy_team):
    teams = [player.team_id for player in fantasy_team]
    frequency = {team: teams.count(team) for team in teams}

    if player.team_id not in frequency.keys():
        return True

    for i in frequency:
        if frequency[i] == player.team_id:
            return False if frequency[i] >= 3 else True
