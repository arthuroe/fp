from api.models import FantasyTeamPlayers, Player, PlayerGameWeek, FantasyTeamPlayerGameWeek
# from api.models import PlayerGameWeek, GameWeek, FantasyTeam, Player, FantasyTeamPlayerGameWeek


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
            player_id=player.player_id, fantasyteam_id=fantasy_team.id).all()

        if player.game_week_id == int(game_week_id):
            fantasy_team_gameweek_info = FantasyTeamPlayerGameWeek.find_first(
                player_gameweek_id=player.id)

            if not fantasy_team_gameweek_info.is_sub:
                points += fantasy_team_gameweek_info.points

            info = player.player_info
            jersey = info.team.jersey
            info = info.serialize()
            info.update({"jersey": jersey})
            player = player.serialize()
            fantasy_team_gameweek_info = fantasy_team_gameweek_info.serialize()
            player.update({"info": info})
            player.update(
                {"gameweek_fantasy_team_info": fantasy_team_gameweek_info})
            team.append(player)

    return team, points


def get_top_players_in_category(players, position, number_of_players):
    players = players.join(PlayerGameWeek.player_info, aliased=True).filter_by(
        position=position).order_by(
        PlayerGameWeek.gameweek_points.desc()).limit(number_of_players).all()
    return players


def update_fantasy_player_gameweek(player, gameweek_stats):
    fantasy_teams = player.fantasy_teams

    for fantasy_team in fantasy_teams:
        try:
            fantasy_player_gameweek = FantasyTeamPlayerGameWeek.filter_by(
                player_gameweek_id=gameweek_stats.id,
                fantasy_team_id=fantasy_team.id
            ).all()

            if not fantasy_player_gameweek:
                gameweek_stats.fantasy_teams.append(fantasy_team)
                gameweek_stats.save()

            fantasy_player = FantasyTeamPlayers.filter_by(
                fantasyteam_id=fantasy_team.id).filter_by(
                player_id=player.id).all()

            fantasy_player_gameweek = FantasyTeamPlayerGameWeek.filter_by(
                player_gameweek_id=gameweek_stats.id,
                fantasy_team_id=fantasy_team.id
            ).all()

            fantasy_player_gameweek[0].is_sub = fantasy_player[0].is_sub
            fantasy_player_gameweek[0].is_captain = fantasy_player[0].is_captain
            fantasy_player_gameweek[0].is_vice_captain = fantasy_player[0].is_vice_captain
            fantasy_player_gameweek[0].points = gameweek_stats.gameweek_points

            if fantasy_player[0].is_captain:
                fantasy_player_gameweek[0].points = fantasy_player_gameweek[0].points * 3
            if fantasy_player[0].is_vice_captain:
                fantasy_player_gameweek[0].points = fantasy_player_gameweek[0].points * 2
            fantasy_player_gameweek[0].save()
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': ("Failed to update player "
                            f"{player} stats in fantasy team {fantasy_team}.")
            }
            return make_response(jsonify(response)), 500
