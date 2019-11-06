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
    season_id = db.Column(db.Integer, db.ForeignKey(
        'seasons.id'), nullable=False)
