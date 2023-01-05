# IMAGE RECOGNITION UTIL USING TF/KERAS
# 
# most of this application adapted from the following walkthrough:
# https://towardsdatascience.com/how-to-use-a-pre-trained-model-vgg-for-image-classification-8dd7c4a4a517

import sys, os
from predict import predict
from keras.applications.vgg16 import VGG16

# declare model to be used for each prediction
model = VGG16(weights='imagenet')

# receive directory path as CLI argument and get a list of all files in path
path = sys.argv[1]
files = os.listdir(path)

# store all results in one list
all_results = []

# for each file in directory, append its prediction result to main list
for file in files:
    result = predict(model, file)
    all_results.append({ path: file, result: result })

print(all_results)
