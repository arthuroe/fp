from api.models import db, ModelMixin


class Team(ModelMixin):
    """
    Team model attributes
    """
    __tablename__ = 'teams'

    name = db.Column(db.String(120), nullable=False)
    logo = db.Column(db.String(180))
    league_position = db.Column(db.Integer)
    manager = db.Column(db.String(180))
    players = db.relationship("Player", backref="team", lazy="dynamic")
