from api.models import db, ModelMixin


class FantasyTeamPlayers(ModelMixin):
    """
    Fantasy Team players model attributes
    """
    __tablename__ = 'fantasy_team_players'

    fantasyteam_id = db.Column(
        'fantasyteam_id', db.Integer, db.ForeignKey('fantasy_teams.id'))
    player_id = db.Column('player_id', db.Integer, db.ForeignKey('players.id'))
    is_sub = db.Column(db.Boolean, default=False)
    is_captain = db.Column(db.Boolean, default=False)
    is_vice_captain = db.Column(db.Boolean, default=False)
