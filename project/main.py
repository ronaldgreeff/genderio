import os
from .helpers_utils import save_image, dtdob
from flask import Flask, request
from flask import jsonify
from flask import render_template
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from . import db
from .models import User, Baby, BabyImg
from .main_forms import NewBabyForm, UpdateBabyForm


main = Blueprint('main', __name__)

# keras disabled for now
# from .helpers_keras import fetch_model
# model = fetch_model()


@main.route("/", methods=["GET"])
def index():
    return render_template("welcome.html")


@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """
    User baby dashboard
    GET serves a list of existing babies for user + new baby form
    POST validates new baby form
    """
    if request.method == "POST":
        dob = dtdob(request.form.get('dob'))
        baby = Baby(
            name=request.form.get('name'),
            dob=dob,
            gender=request.form.get('gender'),
            parent_id=current_user.id,
        )
        db.session.add(baby)
        db.session.commit()

    babies = db.session.query(Baby).filter(Baby.parent_id==current_user.id).all()

    babies = [{'data': {'baby': baby, 'babypics': baby.images}, 'form': UpdateBabyForm()} for baby in babies]

    return render_template("dashboard.html", babies=babies, new=NewBabyForm())


@main.route("/update_baby", methods=["POST"])
@login_required
def make_baby(user_id, baby_id):
    data = {}
    return jsonify(data)


@main.route("/upload_img", methods=["POST"])
@login_required
def upload_img(user_id):
    data = {}
    return jsonify(data)


@main.route("/predict", methods=["POST"])
@login_required
def predict(user_id, baby_id):
    data = {}
    return data

# @main.route("/predict", methods=["POST"])
# @login_required
# def predict():
#
#     data = {"success": False}
#
#     data['form'] = request.form
#     image = request.files.get('image')
#     image_type = request.form.get('imageType')
#
#     img = save_image(image, image_type)
#     if img:
#         data['success'] = True
#
#     return jsonify(data)
