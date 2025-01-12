from flask import Blueprint, request, jsonify, current_app, url_for
from models.UserModel import UserModel
import jwt
import requests
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import secrets


auth_bp = Blueprint('auth', __name__)
user_model = UserModel()
mail = Mail()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"Received data: {data}")

        if not data or not data.get('email') or not data.get('password') or not data.get('username'):
            return jsonify({'error': 'Missing required fields'}), 400

        if user_model.fetch_user_by_email(data['email']):
            return jsonify({'error': 'Email already registered'}), 400

        username = data.get('username', data['email'].split('@')[0])

        user = user_model.create_user(
            name=username,
            email=data['email'],
            password=data['password']
        )
        print(f"Created user: {user}")  

        if not user:
            return jsonify({'error': 'Failed to create user'}), 500

        token = user_model.generate_token(user['id'])

        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': user
        }), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/oauth/google', methods=['POST'])
def google_login():
    data = request.get_json() or request.form
    if not data.get('email'):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        user = user_model.fetch_user_by_email(data['email'])
        if not user:
            user = user_model.create_user(
                name=data.get('name', data['email'].split('@')[0]),
                email=data['email'],
                picture=data.get('picture'),
                oauth_provider='google'
            )
        
        token = user_model.generate_token(user['id'])
        return jsonify({
            'token': token, 
            'user': user,
            'requires_password_set': user['Password'] == ''
        }), 200
    except Exception as e:
        print(f"Error in Google login: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/oauth/github', methods=['POST'])
def github_oauth():
    data = request.get_json()
    if not data or not data.get('code'):
        return jsonify({'error': 'GitHub OAuth code is missing'}), 400

    github_code = data.get('code')
    
    client_id = ""
    client_secret = ""
    redirect_uri = ""
    
    token_url = "https://github.com/login/oauth/access_token"
    
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': github_code,
        'redirect_uri': redirect_uri
    }
    
    headers = {
        'Accept': 'application/json'
    }

    try:
        token_response = requests.post(token_url, data=token_data, headers=headers)
        
        if token_response.status_code != 200:
            return jsonify({'error': 'Failed to authenticate with GitHub'}), 400
        
        token_info = token_response.json()
        print(f"Token info: {token_info}")
        
        if 'access_token' not in token_info:
            return jsonify({'error': 'GitHub OAuth failed to retrieve access token'}), 400
        
        access_token = token_info['access_token']
        user_url = "https://api.github.com/user"
        
        user_headers = {
            'Authorization': f'token {access_token}'
        }

        user_response = requests.get(user_url, headers=user_headers)
        
        if user_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch user data from GitHub'}), 400
        
        github_user = user_response.json()
        
        user = user_model.fetch_user_by_email(github_user['email'])
        
        if not user:
            username = github_user.get('login', github_user['email'].split('@')[0])
            user = user_model.create_user(
                name=username,
                email=github_user['email'],
                picture=github_user.get('avatar_url')
            )
        
        token = user_model.generate_token(user['id'])
        
        return jsonify({
            'token': token,
            'user': user
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json() or request.form
    if not all(key in data for key in ('email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        user = user_model.authenticate_user(data['email'], data['password'])
        if user:
            token = user_model.generate_token(user['id'])
            return jsonify({'token': token, 'user': user}), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    if not data or not all(key in data for key in ('user_id', 'old_password', 'new_password')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    success, message = user_model.change_password(data['user_id'], data['old_password'], data['new_password'])
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    if not data or not all(key in data for key in ('email', 'new_password')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    success, message = user_model.reset_password(data['email'], data['new_password'])
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    if not data or not data.get('email'):
        return jsonify({'error': 'Email is required'}), 400
    
    
    email = data['email']
    try:
        user = user_model.fetch_user_by_email(email)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404

        print(f"User: {user}")        
        password_length = 13


        new_password = secrets.token_urlsafe(password_length)
        
        print(f"User: {user}")        
        
        success, message = user_model.reset_password(user['id'], new_password)
        
        if not success:
            
            return jsonify({'error': message}), 500
        
        
        # Send email with the new password
        msg = Message('Your New Password',
                      sender='noreply@commitbridge.com',
                      recipients=[email])
        
        msg.html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 5px;">
                    <h2 style="color: #4a4a4a;">CommitBridge Password Reset</h2>
                    <p>Hello,</p>
                    <p>We've generated a new password for your CommitBridge account:</p>
                    <p style="background-color: #e9e9e9; padding: 10px; border-radius: 3px; font-family: monospace; font-size: 16px;">{new_password}</p>
                    <p>For security reasons, we recommend changing this password after logging in.</p>
                    <p>If you didn't request this password reset, please contact our support team immediately.</p>
                    <p>Best regards,<br>The CommitBridge Team</p>
                </div>
            </body>
        </html>
        """
        
        mail.send(msg)
        
        return jsonify({'message': 'New password has been sent to your email'}), 200
    except Exception as e:
        print(f"Error in forgot_password: {e}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500


@auth_bp.route('/reset-password-confirm/<token>', methods=['POST'])
def reset_password_confirm(token):
    data = request.get_json()
    if not data or not data.get('new_password'):
        return jsonify({'error': 'New password is required'}), 400
    
    success, message = user_model.reset_password(token, data['new_password'])
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@auth_bp.route('/set-password', methods=['POST'])
def set_password():
    data = request.get_json()
    if not data or not all(key in data for key in ('user_id', 'new_password')):
        return jsonify({'error': 'User ID and new password are required'}), 400
    
    success, message = user_model.set_password(data['user_id'], data['new_password'])
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

