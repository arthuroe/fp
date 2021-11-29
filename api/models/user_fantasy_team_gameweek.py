from api.models import db, ModelMixin


class UserFantasyTeamGameWeek(ModelMixin):
    """
    User Fantasy Team Game Week model attributes
    """
    __tablename__ = 'user_fantasy_team_gameweek'

    transfers = db.Column(db.Integer, default=2)
    points_deductible = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fantasy_team_id = db.Column(db.Integer,
                                db.ForeignKey('fantasy_teams.id'))
    game_week_id = db.Column(db.Integer, db.ForeignKey(
        'gameweeks.id'), nullable=False)
    game_week_points = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
