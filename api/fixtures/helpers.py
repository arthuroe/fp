def get_player_stats(players, fixture):
    home_team, away_team = [], []
    for player in players:
        player_info = player.player_info.serialize()
        serialized_player = player.serialize()
        serialized_player.update({"player_info": player_info})
        if fixture.home_team_id == player.player_info.team.id:
            home_team.append(serialized_player)
        if fixture.away_team_id == player.player_info.team.id:
            away_team.append(serialized_player)
    return home_team, away_team
