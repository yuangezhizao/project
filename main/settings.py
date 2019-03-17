import os
import sys
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'esterTion')

    UPLOAD_PATH = os.path.join(basedir, 'uploads')

    PHOTO_SIZE = {'small': 400,
                  'medium': 800}

    PHOTO_SUFFIX = {
        PHOTO_SIZE['small']: '_s',  # thumbnail
        PHOTO_SIZE['medium']: '_m',  # display
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WHOOSHEE_MIN_STRING_LEN = 1

    REMEMBER_COOKIE_NAME = 'remember_token'
    REMEMBER_COOKIE_DURATION = timedelta(days=365)
    # REMEMBER_COOKIE_DOMAIN
    # REMEMBER_COOKIE_PATH
    REMEMBER_COOKIE_SECURE = 'True'
    REMEMBER_COOKIE_HTTPONLY = 'True'
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = 'True'
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False

    WHOOSHEE_MEMORY_STORAGE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in-memory database


class ProductionConfig(BaseConfig):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
