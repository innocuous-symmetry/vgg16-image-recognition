# IMAGE RECOGNITION UTIL USING TF/KERAS
# 
# most of this application adapted from the following walkthrough:
# https://towardsdatascience.com/how-to-use-a-pre-trained-model-vgg-for-image-classification-8dd7c4a4a517

import sys, os, json, time
from predict import predict
from keras.applications.vgg16 import VGG16

print("\n\n\n")
print("Imports successful! Running startup processes...")

# generate current time for use in identifying outfiles
cur_time = str(int(time.time()))

# create the target directory if it doesn't exist
if (not os.path.exists("./predictions")):
    print("Did not find predictions directory, creating...")
    os.makedirs("./predictions")

# declare model to be used for each prediction
model = VGG16(weights='imagenet')

# receive directory path as CLI argument and get a list of all files in path
path = sys.argv[1]
if (path[-1] != "/"):
    path += "/"

files = os.listdir(path)

# store all results in one list
all_results = []

print("Running image analysis. This may take some time")

# for each file in directory, append its prediction result to main list
for file in files:
    result = predict(model, path + file)
    if result is not None:
        all_results.append({ "path": file, "prediction": result })

print("Analysis complete! Writing JSON to ./predictions/predictions" + cur_time + ".json")

# convert object to JSON and write to JSON file
with open("./predictions/predictions" + cur_time + ".json", "w") as outfile:
    json.dump(all_results, outfile)

print("Process complete!")
