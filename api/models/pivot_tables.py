from api.models import db

db.Table('fantasyteam_players',
         db.Column('fantasyteam_id', db.Integer,
                   db.ForeignKey('fantasy_teams.id')),
         db.Column('player_id', db.Integer, db.ForeignKey('players.id'))
         )

db.Table('season_teams',
         db.Column('season_id', db.Integer,
                   db.ForeignKey('seasons.id')),
         db.Column('team_id', db.Integer, db.ForeignKey('teams.id'))
         )
