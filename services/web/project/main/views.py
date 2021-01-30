import os
from ..helpers.utils import get_img_filename, save_image, dtdob
from flask import Flask, request, send_from_directory, redirect, url_for, flash
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


def flash_errors(form_errors):
    for k, v in form_errors.items():
        flash("Error: {} - {}".format(k, v[0]), "danger")


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

    if not current_user.confirmed:
        return redirect(url_for('auth.unconfirmed'))

    babies = db.session.query(Baby).filter(Baby.parent_id == current_user.id).all()

    if not babies:
        message = "Start by adding your baby's photos below. If your baby has any siblings, you can increase prediction accuracy by adding their scans first."
        flash(message, "success")

    babies = [{
        'baby': baby,
        'babypics': [b.filepath for b in baby.images[:5]],
        'updateform': UpdateBabyForm(id=baby.id),
        'confirmform': ConfirmationForm(id=baby.id),
    } for baby in babies]

    return render_template("dashboard.html", babies=babies, new=NewBabyForm())


@main.route("/make_baby", methods=["POST"])
@login_required
def make_baby():
    # dob = dtdob(request.form.get('dob'))
    # baby = Baby(
    #     name=request.form.get('name'),
    #     dob=dob,
    #     gender=request.form.get('gender'),
    #     parent_id=current_user.id,
    # )
    form = NewBabyForm()

    if form.validate_on_submit():
        baby = Baby(
            name=form.name.data,
            dob=form.dob.data,
            parent_id=current_user.id,
        )

        db.session.add(baby)
        db.session.commit()

    else:
        flash_errors(form.errors)

    return redirect("dashboard")


@main.route("/update_baby", methods=["POST"])
@login_required
def update_baby():
    form = UpdateBabyForm()

    if form.validate_on_submit():
        baby = Baby.query.get(form.id.data)
        if baby:
            if baby.parent_id != current_user.id:
                flash("That baby's parent ID isn't your ID", "danger")
            else:
                if form.update.data:
                    baby.name = form.name.data
                    baby.dob = form.dob.data
                    db.session.commit()
                    flash("Baby details updated", "success")

                elif form.delete.data:
                    baby.parent_id = 0
                    db.session.commit()
                    flash("Baby deleted", "warning")
        else:
            flash("Baby ID invalid", "danger")
    else:
        flash_errors(form.errors)

    return redirect("dashboard")


@main.route("/confirm_gender", methods=["POST"])
@login_required
def confirm_gender():

    form = ConfirmationForm()
    if form.validate_on_submit():
        baby = Baby.query.get(form.id.data)
        if baby:
            if baby.parent_id != current_user.id:
                flash("That baby's parent ID isn't your ID", "danger")
            else:
                if form.right.data:
                    baby.gender = baby.predicted_gender
                    db.session.commit()
                    flash("Thanks for confirming =)", "success")

                elif form.wrong.data:
                    reverse = {'m': 'f', 'f': 'm'}
                    baby.gender = reverse[baby.predicted_gender]
                    db.session.commit()
                    flash("Thanks for confirming. It helps us improve =)", "success")

        else:
            flash("Baby ID invalid", "danger")
    else:
        flash_errors(form.errors)

    # if request.method == "POST":
    #     baby_id = request.form.get('id')
    #
    #     baby = Baby.query.get(baby_id)
    #     if baby:
    #         if baby.parent_id == current_user.id:
    #             if request.form.get('right'):
    #                 baby.gender = baby.predicted_gender
    #                 db.session.commit()
    #
    #             elif request.form.get('wrong'):
    #                 reverse = {'m': 'f', 'f': 'm'}
    #                 baby.gender = reverse[baby.predicted_gender]
    #                 db.session.commit()

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

            data['success'] = True
            data['src'] = partial_filepath
        else:
            data['error'] = "Parent ID does not match parent ID of baby"
    else:
        data['error'] = "No baby found with ID {}".format(baby_id)

    return jsonify(data)


# todo: should serve static files with nginx
@main.route("/media/<filename>", methods=["GET"])
@login_required
def send_media(filename):
    return send_from_directory('media', filename)
