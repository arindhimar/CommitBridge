from flask import Blueprint, request, jsonify, current_app
from models.user import User
from services.auth_service import AuthService
import jwt
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.get_by_id(data['user_id'])
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

### 1. Normal Email/Password Registration
@auth_bp.route('/register', methods=['POST'])
def register():
    print("Registering user")
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not data or not data.get('email') or not data.get('password') or not data.get('username'):
            return jsonify({'error': 'Missing required fields'}), 400

        # Check if email is already registered
        if User.get_by_email(data['email']):
            print("Email already registered")
            return jsonify({'error': 'Email already registered'}), 400

        # Use provided username or fallback to part of the email before '@'
        username = data.get('username', data['email'].split('@')[0])

        # Create a new user
        user = User.create_user(
            username=username,
            email=data['email'],
            password=data['password']
        )

        # Generate JWT token with 1-day expiration
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        # Return success response with user details and token
        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': user.to_dict()
        }), 201

    except Exception as e:
        print
        return jsonify({'error': str(e)}), 400
    
    
### 2. Google OAuth Registration
@auth_bp.route('/oauth/google', methods=['POST'])
def google_oauth():
    data = request.get_json()
    if not data or not data.get('email'):
        return jsonify({'error': 'Invalid data provided'}), 400

    try:
        user = User.get_by_email(data['email'])
        if not user:
            username = data.get('name', data['email'].split('@')[0])
            user = User.create_user(
                username=username,
                email=data['email'],
                picture=data.get('picture')
            )

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, current_app.config['SECRET_KEY'])

        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

### 3. GitHub OAuth Registration
@auth_bp.route('/oauth/github', methods=['POST'])
def github_oauth():
    data = request.get_json()
    if not data or not data.get('email'):
        return jsonify({'error': 'Invalid data provided'}), 400

    try:
        user = User.get_by_email(data['email'])
        if not user:
            username = data.get('name', data['email'].split('@')[0])
            user = User.create_user(
                username=username,
                email=data['email'],
                picture=data.get('avatar_url')  # GitHub's picture field
            )

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, current_app.config['SECRET_KEY'])

        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

