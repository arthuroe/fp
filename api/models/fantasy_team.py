from api.models import db, ModelMixin


class FantasyTeam(ModelMixin):
    """
    Fantasy Team model attributes
    """
    __tablename__ = 'fantasy_teams'

    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    points = db.Column(db.Integer, default=0)
    money = db.Column(db.Integer, default=100)
    season_id = db.Column(db.Integer, db.ForeignKey(
        'seasons.id'), nullable=False)
    captain = db.Column(db.Integer)
    vice_captain = db.Column(db.Integer)
