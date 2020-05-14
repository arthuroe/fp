from api.models import db

db.Table('season_teams',
         db.Column('season_id', db.Integer, db.ForeignKey('seasons.id')),
         db.Column('team_id', db.Integer, db.ForeignKey('teams.id'))
         )
