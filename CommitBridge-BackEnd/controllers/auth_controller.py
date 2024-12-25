from flask import current_app, jsonify
from firebase_admin import auth
from ..models.user import User
from ..services.firestore_service import FirestoreService

class AuthController:
    @staticmethod
    def register_user(email, password, name):
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            new_user = User(id=user.uid, email=email, name=name, provider='email')
            FirestoreService.create_user(new_user)
            return jsonify({'message': 'User registered successfully'}), 201
        except auth.EmailAlreadyExistsError:
            return jsonify({'error': 'Email already exists'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def login_user(email, password):
        try:
            user = auth.get_user_by_email(email)
            # In a real-world scenario, you would verify the password here
            # For simplicity, we're just checking if the user exists
            return jsonify({'token': auth.create_custom_token(user.uid).decode()}), 200
        except auth.UserNotFoundError:
            return jsonify({'error': 'Invalid credentials'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def google_auth(token):
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            new_user = User(id=uid, email=user.email, name=user.display_name, provider='google')
            FirestoreService.create_user(new_user)
            return jsonify({'token': auth.create_custom_token(uid).decode()}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def github_auth(access_token):
        # Implement GitHub authentication logic here
        # This would involve making requests to the GitHub API to get user info
        # and then creating or retrieving the user in your Firestore database
        pass

