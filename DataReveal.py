import json
import matplotlib.pyplot as plt
import collections

def readData():
    data = [[] for i in range(3)]
    with open('Digital_Music_5.json', 'r') as f:
        for line in f:
            record = json.loads(line)
            data[0].append(record['reviewerID'])
            data[1].append(record['asin'])
            data[2].append(record['overall'])
    return data


data = readData()
dict = {}
for key in data[2]:
    dict[key] = dict.get(key, 0) + 1
key_value = list(dict.keys())
value_list = list(dict.values())

plt.bar(key_value, value_list)
plt.title("Rating Score Distribution")
plt.xlabel("Scores")
plt.ylabel("Number of Ratings")
plt.savefig("RatingScoreDistribution.png")
plt.show()

dict = {}
for key in data[0]:
    dict[key] = dict.get(key, 0) + 1
value_list = sorted(list(dict.values()),reverse=True)
plt.plot(range(len(value_list)), value_list)
plt.title("Users' Rating Distribution")
plt.xlabel("Users")
plt.ylabel("Number of Ratings")
plt.savefig("UsersRatingDistribution.png")
plt.show()

dict = {}
for key in data[1]:
    dict[key] = dict.get(key, 0) + 1
value_list = sorted(list(dict.values()),reverse=True)
plt.plot(range(len(value_list)), value_list)
plt.title("Items' Rating Distribution")
plt.xlabel("Items")
plt.ylabel("Number of Ratings")
plt.savefig("ItemsRatingDistribution.png")
plt.show()