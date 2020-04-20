import json
import collections
from math import *
import random

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
        usersCount[key] = ceil(usersCount[key] * 0.8)
    trainData = []
    testData = []
    for record in data:
        if usersCount[record['reviewerID']] > 0:
            if random.randint(0, 1) == 0:
                trainData.append(record)
                usersCount[record['reviewerID']] -= 1
            else:
                testData.append(record)
        else:
            testData.append(record)
    return trainData, testData

def ratePredict(trainData, testData):
    usersAllrate = {}
    users = set()
    for record in trainData:
        user = record['reviewerID']
        users.add(user)
        product = record['asin']
        rate = record['overall']
        if user not in usersAllrate:
            usersAllrate[user] = {}
            usersAllrate[user][product] = rate
        else:
            usersAllrate[user][product] = rate
    # print(usersAllrate['A3EBHHCZO6V2A4'])

    #calculate similarity
    usersSimilar = {}
    for user1 in users:
        res = []
        for user2 in users:
            if user1 != user2:
                similar = Euclidean(usersAllrate[user1], usersAllrate[user2])
                res.append((user2, similar))
        res.sort(key = lambda x: x[1])
        usersSimilar[user1] = [(user, sim) for user, sim in res if sim > 0]
    # print(usersSimilar['A3EBHHCZO6V2A4'])

    # predict test data
    testPredict = {}
    testAllrate = {}
    testUsers = set()
    for record in testData:
        user = record['reviewerID']
        testUsers.add(user)
        product = record['asin']
        rate = record['overall']
        if user not in testPredict:
            testPredict[user] = {}
            testAllrate[user] = {}
            testPredict[user][product] = 0
            testAllrate[user][product] = rate
        else:
            testPredict[user][product] = 0
            testAllrate[user][product] = rate

    # for user in testUsers:
    # ['A1KDEDXOWABBQ6', 'A27LMYOUM86WHY', 'A1A03UKEDEY9IQ', 'A1PJDV044CLYCY', 'A2GRC6IJRA7W4H', 'A3LJ0OBQU01LCL', 'A3VDGERHHLOQVQ', 'A2Y1SCM930PZI7', 'A3F8IKGYL9JQFG', 'A5I1JSA5VN9VG']
    for user in testUsers:
        for product in testPredict[user].keys():
            sumUp = 0
            sumDown = 0
            for simUser, similarity in usersSimilar[user]:
                if product in usersAllrate[simUser]:
                    # print('---------------------')
                    # print(similarity)
                    # print(usersAllrate[simUser][product])
                    sumUp += similarity * usersAllrate[simUser][product]
                    sumDown += similarity
            if sumDown != 0:
                testPredict[user][product] = sumUp / sumDown
            else:
                testPredict[user][product] = -1
    # print(testPredict['A27LMYOUM86WHY'])
    mae = MAE(testPredict, testAllrate)
    print('MAE :', mae)
    rmse = RMSE(testPredict, testAllrate)
    print('RMSE :', rmse)

def MAE(testPredict, testAllrate):
    sumUp = 0
    n = 0
    for user in testPredict.keys():
        for product in testPredict[user]:
            sumUp += abs(testPredict[user][product] - testAllrate[user][product])
            n += 1
    return sumUp / n

def RMSE(testPredict, testAllrate):
    sumUp = 0
    n = 0
    for user in testPredict.keys():
        for product in testPredict[user]:
            sumUp += pow(testPredict[user][product] - testAllrate[user][product], 2)
            n += 1
    return sqrt(sumUp / n)


def Euclidean(rates1, rates2):
    distance = 0
    common = {}
    for key in rates1.keys():
        if key in rates2:
            common[key] = 1
            distance += pow(rates1[key] - rates2[key], 2)
    if len(common) == 0: return 0
    total = len(rates1) + len(rates2) - len(common)
    jac = len(common) / total
    return 1 / (1 + sqrt(distance)) * jac

def pearson_sim(rates1, rates2):
    distance = 0
    common = {}
    for key in rates1.keys():
        if key in rates2:
            common[key] = 1
    if len(common) == 0:
        return 0
    n = len(common)

    sum1 = sum([rates1[key] for key in common])
    sum2 = sum([rates2[key] for key in common])

    sum1sq = sum([pow(rates1[key], 2) for key in common])
    sum2sq = sum([pow(rates1[key], 2) for key in common])

    PSum = sum([rates1[key] * rates2[key] for key in common])

    num = PSum - (sum1 * sum2 / n)
    den = sqrt((sum1sq - pow(sum1, 2) / n) * (sum2sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    return num / den

if __name__ == '__main__':
    data = readData()
    trainData, testData = splitData(data)
    ratePredict(data, testData)
