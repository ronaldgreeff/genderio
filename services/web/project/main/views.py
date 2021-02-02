import os
from flask import Flask, request, redirect, url_for, flash, send_from_directory
from flask import jsonify
from flask import render_template
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from .forms import NewBabyForm, UpdateBabyForm, ConfirmationForm
from .. import db
from ..models import User, Baby, BabyImg
from ..helpers.utils import get_img_filename, save_image, dtdob


main = Blueprint('main', __name__)


def flash_errors(form_errors):
    """General function for flashing errors"""
    for k, v in form_errors.items():
        flash("Error: {} - {}".format(k, v[0]), "danger")


@main.route("/", methods=["GET"])
def index():
    return render_template("welcome.html")


@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """User's dashboard"""

    if not current_user.confirmed:
        return redirect(url_for('auth.unconfirmed'))

    babies = db.session.query(Baby).filter(Baby.parent_id == current_user.id, Baby.deleted == False).all()

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
    """Make a baby"""

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
    """update an existing baby"""

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
                    baby.deleted = True
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
    """Confirm the predicted gender of a baby"""

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

    return redirect("dashboard")


@main.route("/upload_img", methods=["POST"])
@login_required
def upload_img():
    """Upload baby image from dashboard"""

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
            filename = save_image(image, image_type, uid)
            filepath = os.path.join('media', filename)
            baby_img = BabyImg(
                filepath=filepath,
                baby_id=baby.id,
                weeks=weeks,
                days=days,
            )
            db.session.add(baby_img)
            db.session.commit()

            data['success'] = True
            data['src'] = filepath

        else:
            data['error'] = "Parent ID does not match parent ID of baby"
    else:
        data['error'] = "No baby found with ID {}".format(baby_id)

    return jsonify(data)
