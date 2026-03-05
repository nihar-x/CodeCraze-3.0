import os
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_token(email):
    """Generate a signed token for a given email."""
    secret_key = os.getenv("SECRET_KEY", "your-default-secret-key")
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt="magic-link-salt")

def verify_token(token, expiration=600):
    """Verify a signed token and extract the email.
    
    Returns the email if valid, else None.
    'expiration' is in seconds (default 600s = 10 minutes).
    """
    secret_key = os.getenv("SECRET_KEY", "your-default-secret-key")
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(
            token,
            salt="magic-link-salt",
            max_age=expiration
        )
        return email
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return None
