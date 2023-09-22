from functools import wraps
from flask import abort, request
from modules.logic import get_token

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if not 'Authorization' in request.headers:
               abort(401)

            token = request.headers.get('Authorization') 
            real_token = f'Bearer {get_token()}'
            if token != real_token:
                abort(401)

            return f(*args, **kws)            
    return decorated_function



