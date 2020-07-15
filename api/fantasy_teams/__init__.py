from flask import Blueprint

from .views import (
    FantasyTeamView, PlayerFantasyTeamView, CaptainView, ViceCaptainView,
    StartingPlayersView, AddMultiplePlayerView
)

fantasy_team_blueprint = Blueprint(
    'fantasy_teams', __name__, url_prefix='/api/v1')

fantasy_team_view = FantasyTeamView.as_view('fantasy_team_api')
fantasy_team_blueprint.add_url_rule(
    '/fantasy_teams', view_func=fantasy_team_view, methods=['GET', 'POST'])
fantasy_team_blueprint.add_url_rule(
    '/fantasy_teams/<fantasy_team_id>', view_func=fantasy_team_view,
    methods=['GET', 'PUT']
)

fantasy_team_players_view = PlayerFantasyTeamView.as_view(
    'player_fantasy_team_api')
fantasy_team_blueprint.add_url_rule(
    '/fantasy_team_players/<fantasy_team_id>',
    view_func=fantasy_team_players_view,
    methods=['GET', 'POST', 'PUT', 'DELETE']
)

fantasy_team_captain_view = CaptainView.as_view(
    'fantasy_team_captain_api')
fantasy_team_blueprint.add_url_rule(
    '/fantasy_team_captain',
    view_func=fantasy_team_captain_view,
    methods=['GET', 'POST']
)

fantasy_team_vice_captain_view = ViceCaptainView.as_view(
    'fantasy_team_vice_captain_api')
fantasy_team_blueprint.add_url_rule(
    '/fantasy_team_vice_captain',
    view_func=fantasy_team_vice_captain_view,
    methods=['GET', 'POST']
)

starting_players_view = StartingPlayersView.as_view(
    'starting_players_api')
fantasy_team_blueprint.add_url_rule(
    '/starting_players',
    view_func=starting_players_view,
    methods=['POST', 'PUT']
)

add_multiple_players_view = AddMultiplePlayerView.as_view(
    'add_bulk_players_api')
fantasy_team_blueprint.add_url_rule(
    '/add_multiple_fantasy_team_players', view_func=add_multiple_players_view,
    methods=['POST']
)
