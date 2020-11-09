from datetime import datetime

from api.models import db, ModelMixin


class Fixture(ModelMixin):
    """
    Fixtures model attributes
    """
    __tablename__ = 'fixtures'

    name = db.Column(db.String(120))
    date = db.Column(db.DateTime, nullable=False)
    home_team_id = db.Column(db.Integer, nullable=False)
    away_team_id = db.Column(db.Integer, nullable=False)
    home_team_result = db.Column(db.Integer)
    away_team_result = db.Column(db.Integer)
    game_week_id = db.Column(db.Integer, db.ForeignKey(
        'gameweeks.id'), nullable=False)
    player_stats = db.relationship(
        'PlayerGameWeek', backref="fixture", lazy="dynamic")
