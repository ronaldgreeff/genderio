import os
from flask import Flask, current_app
from config import Config
from datetime import datetime as dt
from uuid import uuid3, uuid4

# app = Flask(__name__)
# app.config.from_object(Config)

def get_img_filename(user_id):
    return uuid3(uuid4(), str(user_id)).hex

def save_image(image, image_type, filename):
    app = current_app._get_current_object()
    if image and image_type:
        image_type = image_type.split('/')[-1]
        if image_type in app.config['ALLOWED_EXTENSIONS']:
            partial_filepath = os.path.join(app.config['UPLOAD_FOLDER'], "{}.{}".format(filename, image_type))
            filepath = os.path.join(app.root_path, partial_filepath)
            image.save(filepath)

            return partial_filepath


def dtdob(str_time, format='%d-%m-%Y'):
    """Return date object from string"""
    return dt.strptime(str_time, format).date()
