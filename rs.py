import json

def readData():
    data = []
    with open('Digital_Music_5.json', 'r') as f:
        for line in f:
            record = json.loads(line)
            record = {key: record[key] for key in record.keys() & ('reviewerID', 'asin', 'overall')}
            data.append(record)
    print(data[0])
    return data

if __name__ == '__main__':
    data = readData()
