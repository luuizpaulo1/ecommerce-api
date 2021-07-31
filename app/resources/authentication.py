from functools import wraps
from flask import request
import os


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if token != os.getenv('APP_TOKEN'):
            return {'msg': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated
