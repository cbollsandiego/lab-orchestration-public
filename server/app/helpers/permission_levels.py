
from flask import request, jsonify
from functools import wraps
from app import app
from app.models import User
import jwt

def login_req(*role):
    '''
    This is used as a decorator function in routes.py. login_req() is placed underneath the route decorator for each function
    that required a user to be logged in. Different permission levels for different users can also be added, by adding 'admin',
    'instructor', or 'assistant' to the parameters for the function. Access is given to all users that are at the specified
    permission level or above. Note that there is no specification for students, because this is the lowest permission level.
    '''
    def user_required(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_headers = request.headers.get('Authorization', '').split()
            invalid_msg = {
                'message': 'Invalid token. Registeration and / or authentication required',
                'authenticated': False
            }
            if len(auth_headers) != 1:
                return jsonify(invalid_msg), 401
            try:
                token = auth_headers[0]
                print(token)
                header_data = jwt.get_unverified_header(token)
                data = jwt.decode(token, app.config['SECRET_KEY'], [header_data['alg']])
                user = User.query.filter_by(email=data['sub']).first()
                if not user:
                    raise RuntimeError('User not found')
                if role:
                    if role[0] == 'admin':
                        if user.role != 'admin': 
                            return jsonify(invalid_msg), 401 
                    if role[0] == 'instructor':
                        if user.role != 'admin' and user.role != 'instructor': 
                            return jsonify(invalid_msg), 401
                    if role[0] == 'assistant':
                        if user.role != 'admin' and user.role != 'instructor' and user.role != 'assistant':
                            return jsonify(invalid_msg), 401
                return f(user, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify(invalid_msg), 401
            except (jwt.InvalidTokenError, Exception) as e:
                print(e)
                return jsonify(invalid_msg), 401
        return wrapper
    return user_required