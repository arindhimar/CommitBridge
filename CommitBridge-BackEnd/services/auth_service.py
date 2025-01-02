import os
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

class AuthService:
    def verify_google_token(self, token):
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                os.getenv('GOOGLE_CLIENT_ID')
            )
            return {
                'email': idinfo['email'],
                'name': idinfo.get('name'),
                'picture': idinfo.get('picture')
            }
        except ValueError:
            return None

    def github_oauth_flow(self, code):
        try:
            token_response = requests.post(
                'https://github.com/login/oauth/access_token',
                data={
                    'client_id': os.getenv('GITHUB_CLIENT_ID'),
                    'client_secret': os.getenv('GITHUB_CLIENT_SECRET'),
                    'code': code
                },
                headers={'Accept': 'application/json'}
            )
            token_data = token_response.json()
            
            if 'access_token' not in token_data:
                return None

            user_response = requests.get(
                'https://api.github.com/user',
                headers={
                    'Authorization': f"token {token_data['access_token']}",
                    'Accept': 'application/json'
                }
            )
            user_data = user_response.json()

            return {
                'login': user_data['login'],
                'email': user_data.get('email'),
                'access_token': token_data['access_token']
            }
        except Exception as e:
            print(f"GitHub OAuth error: {str(e)}")
            return None

