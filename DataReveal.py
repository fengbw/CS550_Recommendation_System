import json
import matplotlib.pyplot as plt

def readData():
    data = []
    with open('Digital_Music_5.json', 'r') as f:
        for line in f:
            record = json.loads(line)
            record = record['overall']
            data.append(record)
    return data


data = readData()
dict = {}
for key in data:
    dict[key] = dict.get(key, 0) + 1
key_value = list(dict.keys())
value_list = list(dict.values())

plt.bar(key_value, value_list)
plt.title("Rating Score Distribution")
plt.xlabel("Scores")
plt.ylabel("Number of Ratings")
plt.savefig("RatingScoreDistribution.png")
plt.show()

