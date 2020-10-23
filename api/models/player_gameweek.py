from api.models import db, ModelMixin


class PlayerGameWeek(ModelMixin):
    """
    Player Game Week model attributes
    """
    __tablename__ = 'player_gameweeks'

    game_week_id = db.Column(db.Integer, db.ForeignKey(
        'gameweeks.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey(
        'players.id'), nullable=False)
    fixture_id = db.Column(db.Integer, db.ForeignKey(
        'fixtures.id'), nullable=False)
    minutes_played = db.Column(db.Integer, default=0)
    yellow_card = db.Column(db.Boolean, default=False)
    red_card = db.Column(db.Boolean, default=False)
    tries = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)
    starting_appearance = db.Column(db.Boolean, default=False)
    sub_appearance = db.Column(db.Boolean, default=False)
    assists = db.Column(db.Integer, default=0)
    drop_goals = db.Column(db.Integer, default=0)
    penalty_kicks = db.Column(db.Integer, default=0)
    man_of_the_match = db.Column(db.Boolean, default=False)
    gameweek_points = db.Column(db.Integer, default=0)
    fantasy_teams = db.relationship(
        'FantasyTeam', secondary='fantasy_team_player_gameweeks',
        backref='player_gameweeks', lazy='dynamic'
    )
