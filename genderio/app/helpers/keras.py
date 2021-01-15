import keras
from keras.models import load_model
from keras.preprocessing.image import img_to_array
# TODO: just here for the keras tutorial
from keras.applications import ResNet50


def fetch_model():
    print(" * Loading keras model...")
    global model
    # TODO: load own model
    # model = load_model(models/my_model)
    # model.load_weights(models/my_weights)
    model = ResNet50(weights="imagenet")
    print("* Model loaded")
    return model


def prepare_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    return image
