import numpy as np
from keras.utils import load_img, img_to_array
from keras.applications.vgg16 import preprocess_input, decode_predictions

def predict(model, path):
    # receive image path as CLI argument
    img = load_img(path ,color_mode='rgb', target_size=(224, 224))

    # loaded image to np array for model to read
    x = img_to_array(img)
    x.shape
    x = np.expand_dims(x, axis=0)

    # process array and make predictions
    x = preprocess_input(x)
    features = model.predict(x)
    p = decode_predictions(features)

    return p
