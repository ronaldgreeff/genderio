import os
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Config')


def get_img_filenumber():
    media = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    media_files = os.listdir(media)
    if media_files:
        number = int(media_files[-1].split('.')[-2])
        number += 1
        filenumber = '{:04}'.format(number)
        return filenumber
    return '{:04}'.format(0)


def save_image(image, image_type):
    if image and image_type:
        image_type = image_type.split('/')[-1]
        if image_type in app.config['ALLOWED_EXTENSIONS']:
            filenumber = get_img_filenumber()
            filepath = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], "{}.{}".format(filenumber, image_type))
            image.save(filepath)
