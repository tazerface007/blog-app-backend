import os
from functools import wraps
from flask import jsonify


def require_env_var(env_key):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if os.getenv(env_key) is None:
                return jsonify({
                    "error": "Unauthorized",
                    "message": f"Environment variable '{env_key}' is missing."
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator