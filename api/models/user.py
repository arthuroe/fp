import jwt
import logging

from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt

from api import app
from api.models import db, ModelMixin


class User(ModelMixin):
    """
    User model attributes
    """
    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    phone_number = db.Column(db.String(120))
    receive_club_notifications = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    photo = db.Column(db.String(180))
    fantasy_team_created = db.Column(db.Boolean, default=False)
    fantasy_team = db.relationship(
        'FantasyTeam', backref='user', lazy='dynamic')
    favorite_clubs = db.relationship(
        "Team", secondary="user_teams", backref='users_following',
        lazy="dynamic"
    )

    def __init__(self, **kwargs):
        """
        Initializes the user instance
        """
        self.email = kwargs.get('email')
        self.password = self.hash_password(kwargs.get('password'))
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.phone_number = kwargs.get('phone_number')
        self.gender = kwargs.get('gender')
        self.receive_club_notifications = kwargs.get(
            'receive_club_notifications')
        self.is_admin = kwargs.get('is_admin')
        self.photo = kwargs.get('photo')
        self.fantasy_team_created = kwargs.get('fantasy_team_created')

    def hash_password(self, password):
        if password:
            return Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Check the password against its hash to validate it
        """
        return Bcrypt().check_password_hash(self.password, password)

    @staticmethod
    def generate_token(user):
        """
        Generate access token
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=12),
                'iat': datetime.utcnow(),
                'sub': user
            }
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            logging.error(f"An error while generating a token {e}")
            return str(e)

    @staticmethod
    def decode_token(token):
        """
        Decodes the access token from the Authorization header.
        """
        try:
            payload = jwt.decode(
                token, app.config.get('SECRET_KEY'), algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"
