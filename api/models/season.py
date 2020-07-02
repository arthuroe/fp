from datetime import datetime

from api.models import db, ModelMixin


class Season(ModelMixin):
    """
    Season model attributes
    """
    __tablename__ = 'seasons'

    logo = db.Column(db.String(180))
    name = db.Column(db.String(180))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_current = db.Column(db.Boolean, default=False)
    teams = db.relationship("Team", backref="teams",
                            secondary="season_teams", lazy="dynamic")
