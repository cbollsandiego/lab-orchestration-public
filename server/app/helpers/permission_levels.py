from flask_login import current_user
from flask import flash, redirect, url_for
from functools import wraps

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