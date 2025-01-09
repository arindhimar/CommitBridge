from flask import Flask
from flask_cors import CORS
from models import db
from controllers.auth_controller import auth_bp
from controllers.user_controller import user_bp
from controllers.linkedin_integration_controller import linkedin_integration_bp
from controllers.x_integration_controller import x_integration_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS globally and ensure it handles preflight requests correctly
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://56fe-157-10-217-119.ngrok-free.app"], 
                                 "supports_credentials": True, "methods": ["GET", "POST", "OPTIONS"]}})
    
    db.init_app(app)
    
    # Register blueprints for authentication, users, LinkedIn, and X (Twitter)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(linkedin_integration_bp, url_prefix='/api/linkedin')
    app.register_blueprint(x_integration_bp, url_prefix='/api/x')
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
