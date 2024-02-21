# config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super hard to guess string'
    

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = False
    # commented out for mongoDB
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    # 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


config = {
    'default': DevelopmentConfig
}