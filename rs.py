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
    seen = set()
    for record in data:
        if usersCount[record['reviewerID']] > 0:
            if record['reviewerID'] not in seen:
                trainData.append(record)
                usersCount[record['reviewerID']] -= 1
                seen.add(record['reviewerID'])
            else:
                if random.randint(0,1) == 0:
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
                testPredict[user][product] = random.randint(4,5)
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
    if len(common) < 3: return 0
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

def recommendation(trainData, testData):
    usersAllrate = {}
    users = set()
    products = set()
    for record in trainData:
        user = record['reviewerID']
        users.add(user)
        product = record['asin']
        products.add(product)
        rate = record['overall']
        if user not in usersAllrate:
            usersAllrate[user] = {}
            usersAllrate[user][product] = rate
        else:
            usersAllrate[user][product] = rate

    #calculate similarity
    usersSimilar = {}
    for user1 in users:
        res = []
        for user2 in users:
            if user1 != user2:
                similar = Euclidean(usersAllrate[user1], usersAllrate[user2])
                res.append((user2, similar))
        res.sort(key = lambda x: -x[1])
        usersSimilar[user1] = [(user, sim) for user, sim in res if sim > 0]

    # a = ['A1UQQ995IUT7VT', 'ALR35EFI69S5R', 'A1PFFQTU3E65JI', 'AB93M4OWWM59K', 'A14XWAHMBDAC7N']
    # for user in a[:1]:
    #     print(user, " similar users: ")
    #     print(usersSimilar[user])
    #     print(usersAllrate[user])
    #     for u, s in usersSimilar[user]:
    #         print(u)
    #         print(usersAllrate[u])
    #     print('---------------------')

    # truth data
    allProductPredict = collections.defaultdict(list)
    topNTruth = collections.defaultdict(list)
    testUsers = set()
    for record in testData:
        user = record['reviewerID']
        testUsers.add(user)
        product = record['asin']
        products.add(product)
        rate = record['overall']
        topNTruth[user].append(product)
    for user in testUsers:
        for product in usersAllrate[user].keys():
            topNTruth[user].append(product)
    # predict
    # for user in testUsers:
    # u10 = ['A3EBHHCZO6V2A4']
    u10 = list(testUsers)[:10]
    # user = 'A3EBHHCZO6V2A4'
    for user in testUsers:
        for product in products:
            # if product not in usersAllrate[user]:
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
                allProductPredict[user].append((product, sumUp / sumDown))
            else:
                allProductPredict[user].append((product, 0))
    for user in u10:
        allProductPredict[user].sort(key = lambda x: -x[1])
        if len(allProductPredict[user]) > 10:
            allProductPredict[user] = allProductPredict[user][:10]
    print('products:',len(products))
    print('Users',len(users))
    for user in u10:
        print(user, 'product prediction: ')
        print(allProductPredict[user])
        print(topNTruth[user])
    precision, recall, fM = evaluation(testUsers, allProductPredict, topNTruth)
    print(precision, recall, fM)

def evaluation(testUsers, allProductPredict, topNTruth):
    precision = 0
    recall = 0
    fM = 0
    count = 0
    for user in testUsers:
        count += 1
        truth = len(topNTruth[user])
        # print(truth)
        pre = len(allProductPredict[user])
        # print(pre)
        common = 0
        for product, rate in allProductPredict[user]:
            if product in topNTruth[user]:
                common += 1
        precision += common / pre
        recall += common / truth
        if precision + recall == 0:
            fM = 0
        else:
            fM = 2 * precision * recall / (precision + recall)
    return precision / count, recall / count, fM / count


if __name__ == '__main__':
    data = readData()
    trainData, testData = splitData(data)
    ratePredict(trainData, testData)
    recommendation(trainData, testData)
