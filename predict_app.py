import base64
import numpy as np
import io
from PIL import Image
import keras
from keras import backend as K
from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import request
from flask import jsonify
from flask import Flask

# TODO: just here for the keras tutorial
from keras.applications import ResNet50
from keras.applications import imagenet_utils


app = Flask(__name__)
model = None

def get_model():
    print(" * Loading keras model...")
    global model
    # model = load_model(models/my_model)
    # model.load_weights(models/my_weights)
    model = ResNet50(weights="imagenet")
    print("* Model loaded")

def prepare_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    return image



@app.route("/predict", methods=["POST"])
def predict():
    data = {"success": False}
    if request.method == "POST":
        # message = request.get_json(force=True)
        # image = message.get("image")
        image = request.files.get("image")
        print(request.files)
        if image:
            # string to PIL format
            image = image.read()
            image = Image.open(io.BytesIO(image))
            # preprocess
            image = prepare_image(image, (224, 224))
            # classify image
            preds = model.predict(image)

            # keras tutorial
            results = imagenet_utils.decode_predictions(preds)
            data["predictions"] = []
            for (imagenetID, label, prob) in results[0]:
                r = {"label": label, "probability": float(prob)}
                data["predictions"].append(r)

            # prediction = preds.tolist()
            # response = {
            #     'prediction': {
            #         'boy': prediction[0][0],
            #         'girl': prediction[0][1],
            #     }
            # }

            data["success"] = True
            ##################################################################
            # message = request.get_json(force=True)
            # encoded = message['image']
            #
            # decoded = base64.b64decode(encoded)
            # image = Image.open(io.BytesIO(decoded))
            # processed_image = preprocess_image(image, target_size=(224, 224))
            #
            # prediction = model.predict(processed_image).tolist()
            #
            # response = {
            #     'prediction': {
            #         'boy': prediction[0][0],
            #         'girl': prediction[0][1],
            #     }
            # }

    return jsonify(data)
    # return json

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    get_model()
    app.run()
