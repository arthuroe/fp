from api.models import db, ModelMixin


class FantasyLeague(ModelMixin):
    """
    Fantasy League model attributes
    """
    __tablename__ = 'fantasy_leagues'

    name = db.Column(db.String(120), nullable=False)
    fantasy_teams = db.relationship(
        'FantasyTeam', secondary='fantasyleague_teams',
        backref='fantasy_leagues', lazy='dynamic'
    )
