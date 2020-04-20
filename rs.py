import json
import collections

def readData():
    data = []
    with open('Digital_Music_5.json', 'r') as f:
        for line in f:
            record = json.loads(line)
            record = {key: record[key] for key in record.keys() & ('reviewerID', 'asin', 'overall')}
            data.append(record)
    return data

def splitData(data):
    usersCount = collections.defaultdict(int)
    for record in data:
        usersCount[record['reviewerID']] += 1
    for key in usersCount:
        usersCount[key] //= 1.25
    trainData = []
    testData = []
    for record in data:
        if usersCount[record['reviewerID']] > 0:
            trainData.append(record)
            usersCount[record['reviewerID']] -= 1
        else:
            testData.append(record)
    return trainData, testData

if __name__ == '__main__':
    data = readData()
    trainData, testData = splitData(data)
    print(len(trainData), len(testData))
