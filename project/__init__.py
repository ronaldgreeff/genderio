from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
# from flask_login import LoginManager

db = SQLAlchemy()
# login_manager = LoginManager()

def create_app():
    app = Flask(__name__)#, instance_relative_config=False)
    app.config.from_object(Config)

    db.init_app(app)

    # login_manager.init_app(app)
    # with app.app_context():

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app


    # login_manager.init_app(app)
    #
    # with app.app_context():
    #     from . import routes
    #     from . import auth
    #     from .assets import compile_assets
    #
    #     app.register_blueprint(routes.main_bp)
    #     app.register_blueprint(auth.auth_bp)
    #
    #     db.create_all()
    #
    #     if app.config['FLASK_ENV'] == 'development':
    #         compile_assets(app)
    #
    #     return app
