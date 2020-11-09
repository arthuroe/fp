from api.models import Team


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


def get_gameweek_fixtures(gameweek):
    fixtures = gameweek.fixtures.all()
    fixtures = [fixture.serialize() for fixture in fixtures]
    return fixtures
