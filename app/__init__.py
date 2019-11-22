
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


from config import config
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    # with 'strong' setting,
    # Flask-Login will keep track of the client’s IP address and browser agent
    # and will log the user out if it detects a change.”
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    from .models import User

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .auth.auth_providers import OAuthSignIn
    from .auth.facebook_oauth import FacebookSignIn
    from .auth.twitter_oauth import TwitterSignIn
    return app
