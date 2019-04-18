import re


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
