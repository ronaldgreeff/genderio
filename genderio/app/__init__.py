from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'auth.signin'

# TODO: uncommented lines below

def create_app(config_name):

    app = Flask(__name__, static_folder="static",)
    app.config.from_object(config[config_name])

    mail.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message_category = "info"

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .prediction import prediction as prediction_blueprint
    app.register_blueprint(prediction_blueprint)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        return user

    with app.app_context():
        db.create_all()

    return app
