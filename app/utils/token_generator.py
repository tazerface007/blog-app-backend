from datetime import  datetime, timedelta
import jwt  # type: ignore


def generate_token() -> str:
    """Generate a JWT token with an expiration time of 30 minutes."""
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=30),
        'iat': datetime.utcnow(),
        'sub': 'user_id_example'  # Replace with actual user identifier
    }
    secret_key = 'your_secret_key'  # Replace with your actual secret key
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token