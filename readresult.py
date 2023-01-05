import sys, json

path = sys.argv[1]

with open(path) as file:
    contents = json.load(file)

for line in contents:
    prediction = line['prediction']
    for section in prediction:
        for guess in section:
            if (float(guess[2]) > 0.75):
                print(line['path'])
                print("Probable match: " + guess[1])
                print(guess)
                print("\n")
            elif (float(guess[2]) > 0.3):
                print(line['path'])
                print("Potential match: " + guess[1])
                print(guess)
                print("\n")
            # else:
            #     print(line['path'] + ": inconclusive")
            #     print("\n")
