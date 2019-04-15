from api.models import db, ModelMixin


class User(ModelMixin):
    """
    User model attributes
    """
    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    photo = db.Column(db.String(180))
    fantasy_team = db.relationship(
        'FantasyTeam', backref='user', lazy='dynamic')
