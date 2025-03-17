import os
import platform
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Set default Docker host based on platform
    default_docker_host = 'npipe:////./pipe/docker_engine' if platform.system() == 'Windows' else 'unix:///var/run/docker.sock'
    
    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI', 'sqlite:///app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DOCKER_HOST=os.environ.get('DOCKER_HOST', default_docker_host)
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Register docker blueprint only if it's not already registered
    # Use a more reliable method to check for blueprint registration
    registered_blueprints = [bp.name for bp in app.blueprints.values()]
    if 'docker' not in registered_blueprints:
        from app.docker_api import bp as docker_bp
        app.register_blueprint(docker_bp)

    # Add context processor for templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    # Shell context processor
    @app.shell_context_processor
    def make_shell_context():
        from app.models.user import User
        return {'db': db, 'User': User}

    # Create database tables
    with app.app_context():
        db.create_all()

    return app 