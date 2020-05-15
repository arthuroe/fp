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
    minutes_played = db.Column(db.Integer, default=0)
    yellow_cards = db.Column(db.Boolean, default=False)
    red_cards = db.Column(db.Boolean, default=False)
    trys = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)
