from api.models import db, ModelMixin


class FantasyTeam(ModelMixin):
    """
    Fantasy Team model attributes
    """
    __tablename__ = 'fantasy_teams'

    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    points = db.Column(db.Integer)
    money = db.Column(db.Integer)
