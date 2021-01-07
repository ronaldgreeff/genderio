import os
from .helpers_utils import save_image
from flask import Flask, request
from flask import jsonify
from flask import render_template
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from . import db

main = Blueprint('main', __name__)

# keras disabled for now
# from .helpers_keras import fetch_model
# model = fetch_model()


@main.route("/", methods=["GET"])
def index():
    return render_template("welcome.html")

@main.route("/<user_id>", methods=["GET", "POST"])
@login_required
def dashboard(user_id):
    # get user's babies and each baby's imgs
    return render_template("dashboard.html", name=current_user.name)


@main.route("/predict", methods=["POST"])
def predict():

    data = {"success": False}

    data['form'] = request.form
    image = request.files.get('image')
    image_type = request.form.get('imageType')

    img = save_image(image, image_type)
    if img:
        data['success'] = True

    return jsonify(data)

# if __name__ == "__main__":
#     print(("* Loading Keras model and Flask starting server..."))
#     # get_model()
#     app.run()
