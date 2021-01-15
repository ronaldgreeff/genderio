from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'auth.signin'

def create_app():

    app = Flask(__name__)#, instance_relative_config=False)
    app.config.from_object(Config)
    db.init_app(app)

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.signin'

    mail.init_app(app)
    db.init_app(app)#*
    login_manager.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        return user

    # with app.app_context():
    #     db.create_all()

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
