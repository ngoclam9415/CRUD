import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '1933064486976359',
            'secret': '143db00091452e45c0587c3cee0aa1e5'
        },
        'twitter': {
            'id': 'ypDZS7Dzss3eHpTO4yjgybWze',
            'secret': '8DHwFRDINWGpPRH5rjmvukilgPc1tmTBAY5KPWaFZNgWMTT8Qy'
        },
        'email': {
            'id': '',
            'secret': '',
        },
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #                           'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:@localhost:3306/product?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WHOOSH_BASE = "whoosh"
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:@localhost:3306/product_test?charset=utf8mb4"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = True # THIS WIL ALERT AND REINDEX "TEXTINDEX" WHEN DB CHANGE

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

class PageConfig:
    per_page = 10

class MongoDBConfig:
    IP = "localhost"
    PORT = 27017