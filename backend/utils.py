import secrets
from hashlib import sha256


def secret_key():
    key = secrets.token_urlsafe()
    key = sha256(key.encode()).hexdigest()
    return key
