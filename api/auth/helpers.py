import re

from api import app

from itsdangerous import URLSafeTimedSerializer


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
    return f"http://{base_url}/api/v1/auth/reset_password/{token}"


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
