from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'github_username': self.github_username,
            'platform_preferences': self.platform_preferences,
            'dark_mode': self.dark_mode,
            'timezone': self.timezone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @staticmethod
    def create_user(username, email, password=None, **kwargs):
        new_user = User(username=username, email=email, **kwargs)
        if password:
            new_user.set_password(password)
        db.session.add(new_user)
        try:
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == 'password':
                    self.set_password(value)
                else:
                    setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

