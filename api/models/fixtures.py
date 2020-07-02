from datetime import datetime

from api.models import db, ModelMixin


class Fixture(ModelMixin):
    """
    Fixtures model attributes
    """
    __tablename__ = 'fixtures'

    date = db.Column(db.DateTime, nullable=False)
    home_team = db.Column(db.String(180))
    away_team = db.Column(db.String(180))
    home_team_result = db.Column(db.Integer)
    away_team_result = db.Column(db.Integer)
    game_week_id = db.Column(db.Integer, db.ForeignKey(
        'gameweeks.id'), nullable=False)
