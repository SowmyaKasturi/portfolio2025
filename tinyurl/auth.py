from flask import request,abort
from datetime import datetime,timedelta
import jwt
API_KEY = "hi-from-postman"
def check_api_key():
    key = request.headers.get("X-API-Key")
    if API_KEY != key:
        abort(401, description="Unauthorized")

VALID_NAME="hi"
VALID_PASS="pass"
def basic_auth():
    auth= request.authorization
    if auth.username != VALID_NAME or auth.password != VALID_PASS:
        abort(401,description="Unauthorized" )

def generate_token(name):
    return jwt.encode({"name":name,"exp": datetime.utcnow() + timedelta(hours=1)}, API_KEY)

def decode_token(token):
    try:
        return jwt.decode(token,API_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_jwt(f):
    def decorated(*args, **kwds):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            abort(401, description="Missing or invalid token")

        token = auth_header.split(" ")[1]
        
        user_data = decode_token(token)
        if not user_data:
            abort(401, description="Invalid or expired token")
        return f(*args, **kwds)
    return decorated    

