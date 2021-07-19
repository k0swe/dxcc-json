import csv
import json


def getEntityCode(e):
    return e['entityCode']


dxccList = []
with open('dxcc-2020-02.csv', mode='r', encoding='utf8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        row['entityCode'] = int(row['entityCode'])
        row['deleted'] = (row['deleted'] == 'Y')
        row['outgoingQslService'] = (row['outgoingQslService'] == 'Y')
        row['thirdPartyTraffic'] = (row['thirdPartyTraffic'] == 'Y')

        # Continent must be an array for Maldives and Turkey
        temp = row['continent'].split(',')
        row['continent'] = []
        for c in temp:
            row['continent'].append(c.strip())

        temp = row['itu'].split(',')
        row['itu'] = []
        for c in temp:
            row['itu'].append(int(c.strip()))

        temp = row['cq'].split(',')
        row['cq'] = []
        for c in temp:
            row['cq'].append(int(c.strip()))

        dxccList.append(row)

dxccList.sort(key=getEntityCode)
print(json.dumps({'dxcc': dxccList}, ensure_ascii=False, sort_keys=True))
