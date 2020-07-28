from datetime import datetime

from api.models import db, ModelMixin


class GameWeek(ModelMixin):
    """
    Game Week model attributes
    """
    __tablename__ = 'gameweeks'

    date = db.Column(db.DateTime, nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey(
        'seasons.id'), nullable=False)
    is_current = db.Column(db.Boolean, default=False)
    fixtures = db.relationship(
        "Fixture", backref="game_week", lazy="dynamic")
