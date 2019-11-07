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
    fixtures = db.relationship(
        "Fixtures", backref="fixtures", secondary="game_week", lazy="dynamic")
