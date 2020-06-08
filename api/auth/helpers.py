import logging
import re

from itsdangerous import URLSafeTimedSerializer

from api import app
from api.models import Team


def validate_email(email):
    if re.search('[^@]+@[^@]+\.[^@]+', email):
        return True
    return False


def validate_password(password):
    LENGTH = re.compile(r'.{8,}')
    UPPERCASE = re.compile(r'[A-Z]')
    LOWERCASE = re.compile(r'[a-z]')
    DIGIT = re.compile(r'[0-9]')
    ALL_PATTERNS = (LENGTH, UPPERCASE, LOWERCASE, DIGIT)
    return all(pattern.search(password) for pattern in ALL_PATTERNS)


def generate_reset_url(base_url, token):
    return f"https://{base_url}/api/v1/auth/reset_password/{token}"


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def get_user_teams(teams):
    if teams is None:
        teams = []
    try:
        user_teams = []
        for team in teams:
            t = Team.find_first(id=team.get('id'))
            user_teams.append(t)
        return user_teams
    except Exception as e:
        logging.error(f"An error has occurred  {e}")
        return []
