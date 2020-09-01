from api.models import db

db.Table('season_teams',
         db.Column('season_id', db.Integer, db.ForeignKey('seasons.id')),
         db.Column('team_id', db.Integer, db.ForeignKey('teams.id'))
         )

db.Table('user_teams',
         db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
         db.Column('team_id', db.Integer, db.ForeignKey('teams.id'))
         )

db.Table('fantasy_team_player_gameweek',
         db.Column('player_gameweek_id', db.Integer,
                   db.ForeignKey('player_gameweeks.id')),
         db.Column('fantasy_team_id', db.Integer,
                   db.ForeignKey('fantasy_teams.id'))
         )
