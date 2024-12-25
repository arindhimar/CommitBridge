from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commitbridge.db'  # Use your preferred database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=True)
    github_access_token = db.Column(db.String(255), nullable=True)
    github_username = db.Column(db.String(50), nullable=True)
    github_repositories = db.Column(db.JSON, nullable=True)
    platform_preferences = db.Column(db.JSON, nullable=True)
    twitter_access_token = db.Column(db.String(255), nullable=True)
    linkedin_access_token = db.Column(db.String(255), nullable=True)
    post_schedule = db.Column(db.String(50), nullable=True)
    post_format = db.Column(db.Text, nullable=True)
    summary_preference = db.Column(db.String(50), default="brief")
    preferred_language = db.Column(db.String(50), default="English")
    ai_model_choice = db.Column(db.String(50), nullable=True)
    dark_mode = db.Column(db.Boolean, default=False)
    email_notifications = db.Column(db.Boolean, default=True)
    timezone = db.Column(db.String(50), default="UTC")
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    last_posted = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    # Create new user
    new_user = User(
        username=data.get('login') or data.get('name'),  # GitHub uses 'login', Google uses 'name'
        email=data['email'],
        github_access_token=data.get('github_access_token'),
        github_username=data.get('github_username'),
        # Set other fields as needed
    )

    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

