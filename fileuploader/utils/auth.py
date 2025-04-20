import jwt
from flask import abort, request
from datetime import datetime, timedelta
from hashlib import sha256
from models import LoginAuth, UserRoles, User
from functools import wraps

jwt_key="process_each_user"

def get_token(username, role):
    return jwt.encode({
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }, key=jwt_key)

def decode_token(token):
    try:
        return jwt.decode(token, key=jwt_key,algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except Exception:
        return None
    
def require_roles(allowed_roles):
    def role_based_auth(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                abort(401, "Missing auth token")
            user_data = decode_token(token)
            if not user_data:
                abort(403, "Invalid Token")
            if user_data["role"] not in allowed_roles:
                abort(403, "Forbidden: Insufficient role")
            return f(*args, *kwargs)
        return wrapper
    return role_based_auth