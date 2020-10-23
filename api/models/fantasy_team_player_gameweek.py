from api.models import db, ModelMixin


class FantasyTeamPlayerGameWeek(ModelMixin):
    """
    Fantasy Team Player Game Week model attributes
    """
    __tablename__ = 'fantasy_team_player_gameweeks'

    player_gameweek_id = db.Column(
        db.Integer, db.ForeignKey('player_gameweeks.id'))
    fantasy_team_id = db.Column(db.Integer,
                                db.ForeignKey('fantasy_teams.id'))
    is_sub = db.Column(db.Boolean, default=False)
    is_captain = db.Column(db.Boolean, default=False)
    is_vice_captain = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer, default=0)
