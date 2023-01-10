import json, os, shutil
import psycopg2
from pgutil import PGUTIL
from config import Config

def format_result(app_config: Config, json_path):
    # dictionary to hold and later display our results
    insertions_by_label = {}

    data_path = app_config['data_path']

    # if pg_config is not None, run the postgres prediction[0] of this code
    if app_config['pg_dsn']:
        pgutil = PGUTIL(app_config, json_path)

    # if this is True, run the prediction[0] "for line in contents:" below
    sort_by_match_strength = app_config['sort_by_match_strength']

    weak_results = 0
    total_count = 0
    
    # store analysis results in contents
    with open(json_path) as results:
        contents = json.load(results)

    # prepare individual locations for match strengths if sort is enabled
    if sort_by_match_strength:
        for qualifier in ['strong', 'moderate', 'fair', 'weak']:
            if not os.path.exists("./predictions/" + qualifier):
                os.makedirs('./predictions/' + qualifier)

    # handles data for each photo
    for line in contents:
        img_path = data_path + line['path']
        prediction = line['prediction']

        # handles data for first prediction for a given photo
        total_count += 1
        guess_label = prediction[0][0][1]
        match_accuracy = prediction[0][0][2]
        match_strength = 'weak'

        # container for data to ship to pg
        if pgutil:
            conn = psycopg2.connect(app_config['pg_dsn'])
            cur = conn.cursor()

            pgutil.insert_data(cur, {
                "filename": img_path,
                "topprediction": guess_label,
                "matchaccuracy": match_accuracy
            })

            conn.commit()
            cur.close()
            conn.close()
            print("Database insertions successful!")

        # assign value for match strength
        if float(match_accuracy) > 0.9:
            match_strength = 'strong'
        elif float(match_accuracy) > 0.7:
            match_strength = 'moderate'
        elif float(match_accuracy) > 0.4:
            match_strength = 'fair'
        elif match_strength == 'weak':
            weak_results += 1

        # modify variable for path
        match_strength = match_strength + "/"

        if not guess_label in insertions_by_label:
            insertions_by_label[guess_label] = 0

        print(img_path)
        print("./predictions/" + guess_label)

        # copy file to appropriate location, depending on if sorting
        if sort_by_match_strength:
            if (not os.path.exists("./predictions/" + match_strength + guess_label)):
                os.makedirs("./predictions/" + match_strength + guess_label)
            if (not os.path.exists('./predictions/' + match_strength + guess_label + '/' + img_path)):
                shutil.copy(img_path, "./predictions/" + match_strength + guess_label)
                insertions_by_label[guess_label] = insertions_by_label[guess_label] + 1
        else:
            if (not os.path.exists("./predictions/" + guess_label)):
                os.makedirs("./predictions/" + guess_label)
            if (not os.path.exists('./predictions/' + guess_label + '/' + img_path)):
                shutil.copy(img_path, "./predictions/" + guess_label)
                insertions_by_label[guess_label] = insertions_by_label[guess_label] + 1

    
    print(str(weak_results) + " weak result(s) of a total " + str(total_count) + " input(s)\n")
    print("By subject:\n")

    for k, v in insertions_by_label.items():
        print(k + ": " + str(v) + " file(s) found")
