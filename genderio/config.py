from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    # FLASK_APP = 'wsgi.py'
    SECRET_KEY = environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    UPLOAD_FOLDER = 'media'
    ORIGINALS_FOLDER = 'originals'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = environ['APP_MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = environ['APP_MAIL_DEFAULT_SENDER']


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URL') or \
        'sqlite://'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
