import os
from helpers_keras import *
from helpers_utils import *
from flask import Flask, request
from flask import jsonify
from flask import render_template


app = Flask(__name__)
app.config.from_object('config.Config')

model = fetch_model()


@app.route("/",methods=["GET"])
def home(name=None):
    return render_template("index.html", name=name)

@app.route("/predict", methods=["POST"])
def predict():

    data = {"success": False}

    data['form'] = request.form
    image = request.files.get('image')
    image_type = request.form.get('imageType')

    # if image:
    #     imageType = request.form['imageType'].split('/')[-1]
    #     if imageType in ALLOWED_EXTENSIONS:
    #         filenumber = get_img_filenumber()
    #         filepath = os.path.join(app.root_path, UPLOAD_FOLDER, "{}.{}".format(filenumber, imageType))
    #         image.save(filepath)

    # data['prediction'] = predict(image)

    img = save_image(image, image_type)
    if img:
        data['success'] = True

    return jsonify(data)

if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."))
    # get_model()
    app.run()
