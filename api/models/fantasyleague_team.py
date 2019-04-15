from api.models import db, ModelMixin


class FantasyLeagueTeam(ModelMixin):
    """
    Fantasy League Team model attributes
    """
    __tablename__ = 'fantasyleague_teams'

    fantasyteam_id = db.Column(db.Integer, db.ForeignKey('fantasy_teams.id'))
    fantasyleague_id = db.Column(
        db.Integer, db.ForeignKey('fantasy_leagues.id'))
    points = db.Column(db.Integer)
