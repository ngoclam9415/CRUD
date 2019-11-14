
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    from app.CRUD.city.views import city_blueprint
    from app.CRUD.district.views import district_blueprint
    from app.CRUD.color.views import color_blueprint
    from app.CRUD.category.views import category_blueprint
    from app.CRUD.store.views import store_blueprint
    from app.CRUD.address.views import address_blueprint
    from app.CRUD.product.views import product_blueprint
    from app.CRUD.brand.views import brand_blueprint
    from app.CRUD.product_variant.views import variant_blueprint

    app.register_blueprint(city_blueprint, url_prefix='/city')
    app.register_blueprint(district_blueprint, url_prefix='/district')
    app.register_blueprint(color_blueprint, url_prefix='/color')
    app.register_blueprint(category_blueprint, url_prefix='/category')
    app.register_blueprint(store_blueprint, url_prefix='/store')
    app.register_blueprint(address_blueprint, url_prefix='/address')
    app.register_blueprint(product_blueprint, url_prefix='/product')
    app.register_blueprint(brand_blueprint, url_prefix='/brand')
    app.register_blueprint(variant_blueprint, url_prefix='/variants')

    return app
