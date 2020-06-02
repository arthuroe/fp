from api.models import db

db.Table('season_teams',
         db.Column('season_id', db.Integer, db.ForeignKey('seasons.id')),
         db.Column('team_id', db.Integer, db.ForeignKey('teams.id'))
         )

db.Table('user_teams',
         db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
         db.Column('team_id', db.Integer, db.ForeignKey('teams.id'))
         )
