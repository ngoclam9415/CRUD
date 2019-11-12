
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from config import config
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .models import City

    from app.CRUD.city.views import city_blueprint
    app.register_blueprint(city_blueprint, url_prefix='/city')

    from app.CRUD.address.views import address_blueprint
    app.register_blueprint(address_blueprint, url_prefix='/address')

    return app
