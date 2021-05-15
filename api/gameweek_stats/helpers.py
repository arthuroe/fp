import logging

from threading import Thread

from flask import make_response, jsonify

from api.models import FantasyTeamPlayers, Player, PlayerGameWeek, FantasyTeamPlayerGameWeek


def award_points(**kwargs):
    points = 0
    if kwargs.get('tries'):
        points += award_try_points(**kwargs)
    if kwargs.get('starting_appearance'):
        points += 2
    if kwargs.get('sub_appearance'):
        points += 1
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
                player_gameweek_id=player.id, fantasy_team_id=fantasy_team.id)

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
            fantasy_player_gameweek[0].save()
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': ("Failed to update player "
                            f"{player} stats in fantasy team {fantasy_team}.")
            }
            return make_response(jsonify(response)), 500


def add_initial_player_stats(app, fixtures):
    with app.app_context():
        try:
            for fixture in fixtures:
                players = []
                away = fixture.away_team
                home = fixture.home_team
                players.extend(away.players.all())
                players.extend(home.players.all())
                print(len(players))
                add_player_stats(players, fixture)
            return 'Successfully added all player stats'
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Something wrong happened while adding player stats.'
            }
            return make_response(jsonify(response)), 500


def add_player_stats(players, fixture):
    try:
        for player in players:
            stats = None
            check_gameweek_stats_exist = PlayerGameWeek.filter_by(
                player_id=player.id, game_week_id=fixture.game_week_id).all()

            if check_gameweek_stats_exist:
                stats = check_gameweek_stats_exist[0]

            if not check_gameweek_stats_exist:
                kwargs = {
                    "fixture_id": fixture.id,
                    "game_week_id": fixture.game_week_id,
                    "player_id": player.id
                }
                gameweek_stats = PlayerGameWeek(**kwargs)
                gameweek_stats.gameweek_points = award_points(**kwargs)
                gameweek_stats.save()
                stats = gameweek_stats
            update_fantasy_player_gameweek(player, stats)
        return 'Successfully added player fixture player stats'
    except Exception as e:
        logging.error(f"An error has occurred  {e}")
        response = {
            'status': 'fail',
            'message': 'Something wrong happened while adding player stats.'
        }
        return make_response(jsonify(response)), 500
