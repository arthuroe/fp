from api.models import db, ModelMixin


class Player(ModelMixin):
    """
    Team model attributes
    """
    __tablename__ = 'players'

    name = db.Column(db.String(120), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    position = db.Column(db.String(180))
    age = db.Column(db.Integer)
    price = db.Column(db.Integer, default=8)
    points = db.Column(db.Integer)
    availability = db.Column(db.Boolean, default=True)
    fantasy_teams = db.relationship(
        'FantasyTeam', secondary='fantasy_team_players', backref='players',
        lazy='dynamic'
    )
    gameweek_stats = db.relationship(
        'GameWeek', secondary='player_gameweeks', backref='player_stats',
        lazy='dynamic'
    )
    player_gameweeks = db.relationship(
        "PlayerGameWeek", backref="player_info", lazy="dynamic")
