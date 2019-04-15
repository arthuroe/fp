from api.models import db

db.Table('fantasyteam_players',
         db.Column('fantasyteam_id', db.Integer,
                   db.ForeignKey('fantasy_teams.id')),
         db.Column('player_id', db.Integer, db.ForeignKey('players.id'))
         )

db.Table('fantasyleague_teams',
         db.Column('fantasyteam_id', db.Integer,
                   db.ForeignKey('fantasy_teams.id')),
         db.Column('fantasyleague_id', db.Integer,
                   db.ForeignKey('fantasy_leagues.id'))
         )
