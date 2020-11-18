from api.models import Team


def add_fixture_player_stats(fixture):
    home_team, away_team = [], []
    players = fixture.player_stats.filter_by(
        game_week_id=fixture.game_week_id).all()
    for player in players:
        player_info = player.player_info.serialize()
        serialized_player = player.serialize()
        serialized_player.update({"player_info": player_info})
        if fixture.home_team_id == player.player_info.team.id:
            home_team.append(serialized_player)
        if fixture.away_team_id == player.player_info.team.id:
            away_team.append(serialized_player)

    serialized_fixture = fixture.serialize()
    serialized_fixture.update(
        {
            "player_stats": {
                "home_team": home_team, "away_team": away_team
            }
        }
    )
    return serialized_fixture


def get_team_info(fixture):
    home_team_id = fixture['home_team_id']
    away_team_id = fixture['away_team_id']
    home_team = Team.find_first(id=home_team_id)
    away_team = Team.find_first(id=away_team_id)
    fixture.update(
        {"home_team": home_team.serialize(), "away_team": away_team.serialize()}
    )
    del fixture['home_team_id']
    del fixture['away_team_id']
    return fixture
