# app/__init__.py

# third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads

import flask_excel as excel

# local imports
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
images = UploadSet('images', IMAGES)

def create_app(config_name=Config):
    app = Flask(__name__)
    app.config.from_object(config_name)

    Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)
    excel.init_excel(app)
    configure_uploads(app, images)

    from app import models

    from .department import department as department_blueprint
    app.register_blueprint(department_blueprint)

    from .unit import unit as unit_blueprint
    app.register_blueprint(unit_blueprint)

    from .role import role as role_blueprint
    app.register_blueprint(role_blueprint)

    from .trainee import trainee as trainee_blueprint
    app.register_blueprint(trainee_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .level import level as level_blueprint
    app.register_blueprint(level_blueprint)

    from .spinneret import spinneret as spinneret_blueprint
    app.register_blueprint(spinneret_blueprint)

    return app