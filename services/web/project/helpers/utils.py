import os
from flask import Flask, current_app, send_from_directory
from werkzeug.utils import secure_filename
from project.config import Config
from datetime import datetime as dt
from uuid import uuid3, uuid4
from PIL import Image


def get_img_filename(user_id):
    return uuid3(uuid4(), str(user_id)).hex


def save_image(image, image_type, filename):
    """ save original image and save jpg (model trained on jpgs) """
    app = current_app._get_current_object()
    if image and image_type:
        image_type = image_type.split('/')[-1]
        if image_type in app.config['ALLOWED_EXTENSIONS']:

            # store original image in originals folder
            # og_pfp = os.path.join(app.config['ORIGINALS_FOLDER'], "{}.{}".format(filename, image_type))
            # og_fp = os.path.join(app.root_path, og_pfp)
            # image.save(og_fp)
            image.save(os.path.join(app.config['ORIGINALS_FOLDER'], "{}.{}".format(filename, image_type)))

            # convert original to jpg and return filepath
            # img = Image.open(og_fp)
            img = Image.open(os.path.join(app.config['ORIGINALS_FOLDER'], "{}.{}".format(filename, image_type)))
            jpg = img.convert('RGB')
            # jpg_pfp = os.path.join(app.config['MEDIA_FOLDER'], '{}.jpg'.format(filename))
            # jpg.save(os.path.join(app.root_path, jpg_pfp), 'JPEG')
            jpg.save(os.path.join(app.config['MEDIA_FOLDER'], "{}.jpg".format(filename)))

            return os.path.join(app.config['MEDIA_FOLDER'], "{}.jpg".format(filename))


def dtdob(str_time, format='%d-%m-%Y'):
    """Return date object from string"""
    return dt.strptime(str_time, format).date()
