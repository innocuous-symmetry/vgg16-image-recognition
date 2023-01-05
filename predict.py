import numpy as np
from keras.utils import load_img, img_to_array
from keras.applications.vgg16 import preprocess_input, decode_predictions

def predict(model, path):
    # only allow valid file types
    if not (".jpg" in path or ".jpeg" in path):
        return None

    # receive image path as CLI argument
    img = load_img(path, color_mode='rgb', target_size=(224, 224))

    # loaded image to np array for model to read
    x = img_to_array(img)
    x.shape
    x = np.expand_dims(x, axis=0)

    # process array and make predictions
    x = preprocess_input(x)
    features = model.predict(x)
    p = decode_predictions(features)
    
    for predict in p:
        i = 0
        while i < len(predict):
            predict[i] = (predict[i][0], predict[i][1], str(predict[i][2]))
            i = i + 1

    return p
