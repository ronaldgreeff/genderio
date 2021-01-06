import os
from .helpers_utils import save_image
from flask import Flask, request
from flask import jsonify
from flask import render_template
from flask import Blueprint

# app = Flask(__name__)
# app.config.from_object('config.Config')

main = Blueprint('main', __name__)

# disabled for now
# from .helpers_keras import fetch_model
# model = fetch_model()


@main.route("/",methods=["GET"])
def index(name=None):
    return render_template("index.html", name=name)

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
