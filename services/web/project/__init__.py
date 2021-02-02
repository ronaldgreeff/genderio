import os
from flask import Flask, send_from_directory
from flask_login import LoginManager
from flask_mail import Mail
from .config import config
from .models import db


mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'auth.signin'


def create_app():
    """Standard flask factory 'create_app' function"""

    app = Flask(__name__)
    config_name = f"{os.getenv('FLASK_ENV')}" or 'default'
    app.config.from_object(config[config_name])

    mail.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message_category = "info"

    from .main.views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth.views import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # from .prediction.views import prediction as prediction_blueprint
    # app.register_blueprint(prediction_blueprint)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        return user

    @app.route("/static/<path:filename>")
    def staticfiles(filename):
        return send_from_directory(app.config["STATIC_FOLDER"], filename)

    @app.route("/media/<path:filename>")
    def mediafiles(filename):
        return send_from_directory(app.config["MEDIA_FOLDER"], filename)

    with app.app_context():
        db.create_all()

    return app
