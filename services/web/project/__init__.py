import os

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)

from .config import config
from flask_login import LoginManager
from flask_mail import Mail
from .models import db


mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'auth.signin'


# def create_app(config_name):
def create_app():

    app = Flask(__name__)
    config_name = os.getenv('FLASK_ENV') or 'default'
    print(config_name)
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

    with app.app_context():
        db.create_all()

    return app


# app = Flask(__name__)
# app.config.from_object("project.config.Config")
# db = SQLAlchemy(app)
#
#
# class User(db.Model):
#     __tablename__ = "users"
#
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(128), unique=True, nullable=False)
#     active = db.Column(db.Boolean(), default=True, nullable=False)
#
#     def __init__(self, email):
#         self.email = email
#
#
# @app.route("/")
# def hello_world():
#     return jsonify(hello="world")
#
#
# @app.route("/static/<path:filename>")
# def staticfiles(filename):
#     return send_from_directory(app.config["STATIC_FOLDER"], filename)
#
#
# @app.route("/media/<path:filename>")
# def mediafiles(filename):
#     return send_from_directory(app.config["MEDIA_FOLDER"], filename)
#
#
# @app.route("/upload", methods=["GET", "POST"])
# def upload_file():
#     if request.method == "POST":
#         file = request.files["file"]
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
#     return f"""
#     <!doctype html>
#     <title>upload new File</title>
#     <form action="" method=post enctype=multipart/form-data>
#       <p><input type=file name=file><input type=submit value=Upload>
#     </form>
#     """
