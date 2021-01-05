import os
import base64
# KERAS ########################################################################
import numpy as np
from io import BytesIO
from PIL import Image
import keras
from keras import backend as K
from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array
# TODO: just here for the keras tutorial
from keras.applications import ResNet50
from keras.applications import imagenet_utils
# FLASK ########################################################################
from flask import Flask, request, flash
from base64 import urlsafe_b64decode, b64decode
from flask import jsonify
# from werkzeug.utils import secure_filename
from flask import render_template

# SETUP ########################################################################
UPLOAD_FOLDER = 'media'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SECRET_KEY'] = "please_in_the_name_of_jeebus_change_me" # TODO:
model = None

# HELPERS ######################################################################
def get_model():
    print(" * Loading keras model...")
    global model
    # TODO: load own model
    # model = load_model(models/my_model)
    # model.load_weights(models/my_weights)
    model = ResNet50(weights="imagenet")
    print("* Model loaded")

def prepare_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    return image

def get_img_filenumber():
    media = os.path.join(app.root_path, UPLOAD_FOLDER)
    media_files = os.listdir(media)
    if media_files:
        number = int(media_files[-1].split('.')[-2])
        number += 1
        filenumber = '{:04}'.format(number)
        return filenumber
    return '{:04}'.format(0)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
################################################################################


@app.route("/",methods=["GET"])
def home(name=None):
    return render_template("index.html", name=name)

@app.route("/predict", methods=["POST"])
def predict():

    data = {"success": False}

    data['form'] = request.form
    image = request.files.get('image')

    if image:
        imageType = request.form['imageType'].split('/')[-1]
        if imageType in ALLOWED_EXTENSIONS:
            filenumber = get_img_filenumber()
            filepath = os.path.join(app.root_path, UPLOAD_FOLDER, "{}.{}".format(filenumber, imageType))
            image.save(filepath)
            data['success'] = True

    return jsonify(data)

if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."))
    # get_model()
    app.run()
