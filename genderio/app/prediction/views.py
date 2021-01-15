import os
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

from . import prediction

# keras disabled for now
# from .helpers_keras import fetch_model
# model = fetch_model()

# model = load_model(pathlib.Path('models/tl2_final'))
# model.load_weights(pathlib.Path('models/tl2_final.h5'))

def predict_gender(baby):
    d = {'male': [], 'female': []}
    baby_image_filepaths = db.session.query(BabyImg.filepath).filter(BabyImg.baby_id==baby.id).all()
    for baby_image in baby_image_filepaths:
        preds = model.predict(baby_image)
        print("preds", preds)

    # image_paths = [
    #     'boy/286242_5d3ca9f6-8d8a-408c-bade-01a6efddca6d.jpg',
    #     'girl/391126_29455299-9e94-4e02-bd1d-c34e391e9546.jpg'
    # ]
    #
    # preds = []
    #
    # for image_path in image_paths:
    #     image = keras.preprocessing.image.load_img(
    #         pathlib.Path('data/{}'.format(image_path)),
    #         color_mode="grayscale",
    #         target_size=(128, 128),
    #     )
    #     input_array = keras.preprocessing.image.img_to_array(image)
    #     input_array = np.array([input_array])
    #     pred = model.predict(input_array)
    #
    #     cl = np.round(pred)
    #     pr = pred[:,0]
    #
    #     print(pr, cl)

    # query babies images
    # for images in images:
    #    preds = model.predict(image)
    #    results = decode predictions(preds)
    #    for (imagenetID, label, prob) in results[0]:
    #       append to d[gender]
    # if unequal get most and average else get average and highest
    return d

@prediction.route("/predict", methods=["POST"])
@login_required
def predict():
    data = {'success': False, 'error': None}

    baby_id = request.form.get('id')
    baby = Baby.query.get(baby_id)

    if baby:
        if baby.parent_id == current_user.id:
            gender = predict_gender(baby)

            data['success'] = True
            data['gender'] = gender

    return data
