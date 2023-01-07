import json, os, shutil

def format_result(src_path, json_path):
    insertions_by_label = {}

    weak_results = 0
    total_count = 0
    
    with open(json_path) as results:
        contents = json.load(results)

    for qualifier in ['strong', 'moderate', 'fair', 'weak']:
        if not os.path.exists("./predictions/" + qualifier):
            os.makedirs('./predictions/' + qualifier)

    for line in contents:
        img_path = src_path + line['path']
        prediction = line['prediction']
        for section in prediction:
            total_count += 1
            guess_label = section[0][1]
            match_strength = 'weak/'

            if float(section[0][2]) > 0.9:
                match_strength = 'strong/'
            elif float(section[0][2]) > 0.75:
                match_strength = 'moderate/'
            elif float(section[0][2]) > 0.5:
                match_strength = 'fair/'
            elif match_strength == 'weak/':
                weak_results += 1

            if not guess_label in insertions_by_label:
                insertions_by_label[guess_label] = 0

            if (not os.path.exists("./predictions/" + match_strength + guess_label)):
                os.makedirs("./predictions/" + match_strength + guess_label)

            if (not os.path.exists('./predictions/' + match_strength + guess_label + '/' + img_path)):
                shutil.copy(img_path, "./predictions/" + match_strength + guess_label)
                insertions_by_label[guess_label] = insertions_by_label[guess_label] + 1
    
    print(str(weak_results) + " weak result(s) of a total " + str(total_count) + " input(s)\n")
    print("By subject:\n\n")

    for k, v in insertions_by_label.items():
        print(k + ": " + str(v) + " file(s) found")
