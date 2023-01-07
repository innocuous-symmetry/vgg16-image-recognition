# IMAGE RECOGNITION UTIL USING TF/KERAS
# 
# most of this application adapted from the following walkthrough:
# https://towardsdatascience.com/how-to-use-a-pre-trained-model-vgg-for-image-classification-8dd7c4a4a517

import sys, os, json
from time import time
from predict import predict
from formatresult import format_result
from keras.applications.vgg16 import VGG16

print("\n\nImage Sorting Utility\n")
print("Script by Mikayla Dobson\n")
print("\n\n")
print("Begininning setup...\n\n")

############################## SETUP
############################## SETUP
############################## SETUP

# create the target directory if it doesn't exist
if (not os.path.exists("./predictions")):
    print("Did not find predictions directory, creating...\n\n")
    os.makedirs("./predictions")

# receive directory path as CLI argument and get a list of all files in path
src_path = sys.argv[1]

if (src_path[-1] != "/"):
    src_path += "/"

files = os.listdir(src_path)

# generate current time for use in identifying outfiles
cur_time = str(int(time()))

# store all results in one list
all_results = []

############################## ANALYSIS
############################## ANALYSIS
############################## ANALYSIS

# declare model to be used for each prediction
model = VGG16(weights='imagenet')

print("Running image analysis. This may take some time...\n\n")

# for each file in directory, append its prediction result to main list
for file in files:
    result = predict(model, src_path + file)
    if result is not None:
        all_results.append({ "path": file, "prediction": result })

json_path = "./predictions/predictions" + cur_time + ".json"

print("Writing analysis results to " + json_path + "\n\n")

# convert object to JSON and write to JSON file
with open(json_path, "w") as outfile:
    json.dump(all_results, outfile)

print("Analysis complete! Beginning sort process...\n\n")

############################## SORTING
############################## SORTING
############################## SORTING

format_result(src_path, json_path)

print("File sort successful! Process complete.")
