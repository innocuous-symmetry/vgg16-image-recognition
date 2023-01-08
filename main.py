# IMAGE RECOGNITION UTIL USING TF/KERAS
# 
# most of this application adapted from the following walkthrough:
# https://towardsdatascience.com/how-to-use-a-pre-trained-model-vgg-for-image-classification-8dd7c4a4a517

import os, json
from config import Config
from time import time

print("\nImage Sorting Utility\n")
print("Script by Mikayla Dobson\n")
print("\n\n")

############################## CONFIG

print("Running app config...")
appconfig: Config = Config()
config_file = appconfig.run()

if (config_file.get_data_path()[-1] != "/"):
    config_file.set_data_path(config_file.get_data_path() + "/")

# create the target directory if it doesn't exist
if (not os.path.exists("./predictions")):
    print("Did not find predictions directory, creating...\n\n")
    os.makedirs("./predictions")

############################## SETUP
############################## SETUP
############################## SETUP

files = os.listdir(config_file.data_path)

# generate current time for use in identifying outfiles
cur_time = str(int(time()))

# store all results in one list
all_results = []

############################## ANALYSIS
############################## ANALYSIS
############################## ANALYSIS

print("Attempting TF imports...\n\n")

from predict import predict
from formatresult import format_result
from keras.applications.vgg16 import VGG16

print("Success!")

# declare model to be used for each prediction
model = VGG16(weights='imagenet')

print("Running image analysis. This may take some time...\n\n")

# for each file in directory, append its prediction result to main list
for file in files:
    result = predict(model, config_file.data_path + file)
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

format_result(appconfig, json_path)

print("File sort successful! Process complete.")
