from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=True)  # Optional if OAuth is used
    github_access_token = Column(String(255), nullable=False)
    github_username = Column(String(50), nullable=False)
    github_repositories = Column(JSON, nullable=True)  # List of selected repositories
    platform_preferences = Column(JSON, nullable=True)  # JSON: { "twitter": true, "linkedin": false }
    twitter_access_token = Column(String(255), nullable=True)
    linkedin_access_token = Column(String(255), nullable=True)
    post_schedule = Column(String(50), nullable=True)  # E.g., "9:00 AM"
    post_format = Column(Text, nullable=True)  # Customizable template
    summary_preference = Column(String(50), default="brief")
    preferred_language = Column(String(50), default="English")
    ai_model_choice = Column(String(50), nullable=True)  # Optional
    dark_mode = Column(Boolean, default=False)
    email_notifications = Column(Boolean, default=True)
    timezone = Column(String(50), default="UTC")
    last_login = Column(DateTime, default=datetime.utcnow)
    last_posted = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
