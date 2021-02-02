import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/media"
    ORIGINALS_FOLDER = f"{os.getenv('APP_FOLDER')}/project/originals"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    SQLALCHEMY_DATABASE_URI = f"{os.getenv('DATABASE_URL', 'sqlite://')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = f"{os.getenv('MAIL_SERVER')}"
    MAIL_PORT = f"{os.getenv('MAIL_PORT')}"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = f"{os.getenv('APP_MAIL_USERNAME')}"
    MAIL_PASSWORD = f"{os.getenv('APP_MAIL_PASSWORD')}"
    MAIL_DEFAULT_SENDER = f"{os.getenv('APP_MAIL_DEFAULT_SENDER')}"


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"{os.getenv('TEST_DATABASE_URL')}" or \
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
