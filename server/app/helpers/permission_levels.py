from flask_login import current_user
from flask import flash, redirect, url_for, request, jsonify
from functools import wraps
from app import app, db
from app.models import User
import jwt

def login_req(*role):
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


'''All functions below here can be deleted when routes.py is fully converted to be just backend'''
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user == None:
            return redirect(url_for('index'))
        if current_user.role != 'admin':
            flash('Access denied! Admin access required.')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return wrapper

def instructor_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user == None:
            return redirect(url_for('index'))
        if current_user.role != 'admin' and current_user.role != 'instructor':
            flash('Access denied! Instructor access required.')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return wrapper

def assistant_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user == None:
            return redirect(url_for('index'))
        if current_user.role == 'student':
            flash('Access denied! Assistant or greater access required.')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return wrapper