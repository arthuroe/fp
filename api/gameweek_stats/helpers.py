from api.models import FantasyTeamPlayers, Player, PlayerGameWeek


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


def get_fantasy_player_stats(fantasy_team, game_week_id):
    team = []
    points = 0

    gameweeks_players = fantasy_team.player_gameweeks
    fantasy_team_players = fantasy_team.players

    for player in gameweeks_players:
        fantasy_team_info = FantasyTeamPlayers.filter_by(
            id=player.player_id).all()
        fantasy_team_info = fantasy_team_info[0].serialize()
        fantasy_team_info = {
            'is_sub': fantasy_team_info['is_sub'],
            'is_captain': fantasy_team_info['is_captain'],
            'is_vice_captain': fantasy_team_info['is_vice_captain']
        }
        if player.game_week_id == int(game_week_id):
            points += player.gameweek_points
            info = player.player_info
            jersey = info.team.jersey
            info = info.serialize()
            info.update({"jersey": jersey})
            player = player.serialize()
            player.update({"info": info})
            player.update(fantasy_team_info)
            team.append(player)

    return team, points


def get_top_players_in_category(players, position, number_of_players):
    players = players.join(PlayerGameWeek.player_info, aliased=True).filter_by(
        position=position).order_by(
        PlayerGameWeek.gameweek_points.desc()).limit(number_of_players).all()
    return players
