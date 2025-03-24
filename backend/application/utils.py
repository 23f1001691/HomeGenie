from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import  jsonify

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            for role in roles:
                if claims["role"]==role:
                    return fn(*args, **kwargs)
            else:
                return jsonify({'message': 'Unauthorized role'}), 403
        return decorator
    return wrapper

def profile_format(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def resume_format(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

def format_date(date_obj):
    return date_obj.strftime('%Y-%m-%d') if date_obj else None