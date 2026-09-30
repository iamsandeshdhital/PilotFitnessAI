"""
Basic authentication module for Pilot Fitness Assessment AI Tool
"""

from functools import wraps
from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import os


# Simple user store (in production, use database)
USERS = {
    'admin': {
        'password': generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'admin123')),
        'role': 'admin',
    },
    'assessor': {
        'password': generate_password_hash(os.environ.get('ASSESSOR_PASSWORD', 'assessor123')),
        'role': 'assessor',
    },
    'viewer': {
        'password': generate_password_hash(os.environ.get('VIEWER_PASSWORD', 'viewer123')),
        'role': 'viewer',
    },
}


def authenticate(username, password):
    """Authenticate user credentials"""
    user = USERS.get(username)
    if user and check_password_hash(user['password'], password):
        return {'username': username, 'role': user['role']}
    return None


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        if session['user'].get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


def role_required(roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            if session['user'].get('role') not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
