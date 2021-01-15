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
from .forms import NewBabyForm, UpdateBabyForm, ConfirmationForm


main = Blueprint('main', __name__)

# keras disabled for now
# from .helpers_keras import fetch_model
# model = fetch_model()


def predict_gender(baby):
    d = {'male': [], 'female': []}
    baby_image_filepaths = db.session.query(BabyImg.filepath).filter(BabyImg.baby_id==baby.id).all()
    for baby_image in baby_image_filepaths:
        preds = model.predict(baby_image)
        print("preds", preds)
    # query babies images
    # for images in images:
    #    preds = model.predict(image)
    #    results = decode predictions(preds)
    #    for (imagenetID, label, prob) in results[0]:
    #       append to d[gender]
    # if unequal get most and average else get average and highest
    return d

@main.route("/predict", methods=["POST"])
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

# todo: should serve static files with nginx
@main.route("/media/<filename>", methods=["GET"])
@login_required
def send_media(filename):
    return send_from_directory('media', filename)
