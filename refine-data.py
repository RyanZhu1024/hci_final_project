import csv


with open('train.csv', encoding='latin-1') as trainFile:
    reader = csv.reader(trainFile, delimiter=',')
    negdata = open('negdata-all.txt', 'w')
    posdata = open('posdata-all.txt', 'w')
    neudata = open('neudata-all.txt', 'w')
    cnt = 0
    cnt1 = 0
    cnt2 = 0
    cnt3 = 0
    for row in reader:
        cnt += 1
        sentiment = row[0]
        text = row[-1]
        if int(sentiment) is 0:
            negdata.write('%s\n' % text)
            cnt1 += 1
        elif int(sentiment) is 2:
            neudata.write('%s\n' % text)
            cnt2 += 1
        elif int(sentiment) is 4:
            posdata.write('%s\n' % text)
            cnt3 += 1
    negdata.close()
    posdata.close()
    neudata.close()
    print(cnt)
    print(cnt1)
    print(cnt2)
    print(cnt3)





