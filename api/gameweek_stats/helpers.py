from api.models import Player, PlayerGameWeek


def award_points(**kwargs):
    points = 0
    if kwargs.get('tries'):
        points += award_try_points(**kwargs)
    if kwargs.get('starting_appearance'):
        points += 2
    if kwargs.get('sub_appearance'):
        points += 2
    if kwargs.get('man_of_the_match'):
        points += 5
    if kwargs.get('assists'):
        assists = kwargs.get('assists') * 3
        points += assists
    if kwargs.get('conversions'):
        points += kwargs.get('conversions')
    if kwargs.get('penalty_kicks'):
        penalty_kicks = kwargs.get('penalty_kicks') * 2
        points += penalty_kicks
    if kwargs.get('drop_goals'):
        drop_goals = kwargs.get('drop_goals') * 2
        points += drop_goals
    if kwargs.get('yellow_card'):
        points -= 3
    if kwargs.get('red_card'):
        points -= 5
    return points


def award_try_points(**kwargs):
    player = Player.find_first(id=kwargs.get('player_id'))
    if player.position in ['FR', 'SR', 'BR']:
        return kwargs.get('tries') * 6
    return kwargs.get('tries') * 4


def get_fantasy_player_stats(fantasy_team_players, game_week_id):
    player_stats = []
    team_points = 0
    for fantasy_team_player in fantasy_team_players:
        player = PlayerGameWeek.filter_by(
            player_id=fantasy_team_player.id, game_week_id=game_week_id).all()
        player_stats.append(player[0].serialize())
    return player_stats
