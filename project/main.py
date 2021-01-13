import os
from .helpers_utils import get_img_filename, save_image, dtdob
from flask import Flask, request, send_from_directory, redirect
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
    babies = [{
            'baby': baby,
            'babypics': [b.filepath for b in baby.images[:5]],
            'updateform': UpdateBabyForm(id=baby.id)}
        for baby in babies]

    return render_template("dashboard.html", babies=babies, new=NewBabyForm())


@main.route("/update_baby", methods=["POST"])
@login_required
def update_baby():

    # data = {'success': False, 'error': None}
    if request.method == "POST":

        baby_id = request.form.get('id')
        name = request.form.get('name')
        dob = dtdob(request.form.get('dob'))

        baby = Baby.query.get(baby_id)
        if baby:
            if baby.parent_id == current_user.id:
                if request.form.get('update'):

                    baby.name = name
                    baby.dob = dob
                    db.session.commit()

                elif request.form.get('delete'):

                    baby.parent_id = 0
                    db.session.commit()

        #         data['success'] = True
        #     else:
        #         data['error'] = "Parent ID does not match parent ID of baby"
        # else:
        #     data['error'] = "No baby found with that ID"

    # return jsonify(data)
    return redirect("dashboard")


@main.route("/upload_img", methods=["POST"])
@login_required
def upload_img():

    data = {'success': False, 'error': None}

    image = request.files.get('image')
    image_type = request.form.get('imageType')
    baby_id = request.form.get('baby_id')
    weeks = request.form.get('weeks')
    days = request.form.get('days')

    baby = Baby.query.get(baby_id)

    if baby:
        if baby.parent_id == current_user.id:
            uid = get_img_filename(current_user.id)
            partial_filepath = save_image(image, image_type, uid)
            baby_img = BabyImg(
                filepath=partial_filepath,
                baby_id=baby.id,
                weeks=weeks,
                days=days,
            )
            db.session.add(baby_img)
            db.session.commit()

            # filepath = save_image(image, image_type, filename)
            data['success'] = True
            data['src'] = partial_filepath
        else:
            data['error'] = "Parent ID does not match parent ID of baby"
    else:
        data['error'] = "No baby found with that ID"


    return jsonify(data)

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
