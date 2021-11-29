from api.models import UserFantasyTeamGameWeek, GameWeek, FantasyTeam


def create(**kwargs):
    pass

def get(game_week_id, user_id):
    return UserFantasyTeamGameWeek.find_first(user_id=user_id, game_week_id=game_week_id)