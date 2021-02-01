import os
import pathlib
import numpy as np
from ..helpers.utils import get_img_filename, save_image, dtdob
from flask import Flask, request, send_from_directory, redirect, url_for
from flask import jsonify
from flask import render_template
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from .. import db
from ..models import User, Baby, BabyImg

import keras
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

# from . import prediction
from .tokens import generate_outcome_token, deserialize_outcome_token


prediction = Blueprint('prediction', __name__)

# keras disabled for now
# from .helpers_keras import fetch_model
# model = fetch_model()

model = load_model(os.path.join(os.getcwd(), 'project/prediction/models/tl2_final'))
model.load_weights(os.path.join(os.getcwd(), 'project/prediction/models/tl2_final.h5'))


def predict_gender(baby):

    gender_classes = {0: 'm', 1: 'f'}

    baby_image_filepaths = db.session.query(
        BabyImg.filepath
    ).filter(
        BabyImg.baby_id == baby.id
    ).all()

    predictions = {0: 0, 1: 0}

    for baby_image in baby_image_filepaths:
        baby_image_path = os.path.join(os.getcwd(), 'project', baby_image[0])
        image = keras.preprocessing.image.load_img(
            baby_image_path,
            color_mode="grayscale",
            target_size=(128, 128),
        )
        input_array = keras.preprocessing.image.img_to_array(image)
        input_array = np.array([input_array])
        pred = model.predict(input_array)

        cls = int(pred[:, 0][0])

        predictions[cls] += 1

    predicted_gender_cls = max(predictions, key=predictions.get)
    predicted_gender = gender_classes[predicted_gender_cls]

    return predicted_gender


@prediction.route("/predict", methods=["POST"])
@login_required
def predict():

    baby_id = request.form.get('button')
    baby = Baby.query.get(baby_id)

    if baby:
        if baby.parent_id == current_user.id:
            predicted = predict_gender(baby)
            baby.predicted_gender = predicted
            db.session.commit()

    return redirect(url_for('main.dashboard'))


@prediction.route("/outcome/<token>")
def confirm_outcome(token):

    oc = request.args.get('oc')
    print(oc, token)
    # token = request.args.get('token')

    if oc is not None and token:
        data = deserialize_outcome_token(token)

        if data:
            parent_email = data.get('parent_email')
            baby_id = data.get('baby_id')

            baby = db.session.query(
                Baby
            ).join(
                User
            ).filter(
                Baby.id == baby_id,
                User.email == parent_email,
            ).first_or_404()

            if oc:
                baby.gender = baby.predicted_gender
            else:
                reverse = {'m': 'f', 'f': 'm'}
                baby.gender = reverse[baby.predicted_gender]
            db.session.commit()

            # todo: an actual page
            return "Thanks!"

    return "Invalid"
