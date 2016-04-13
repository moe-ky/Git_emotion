from scipy.stats.stats import pearsonr
import csv
from Dictionary_search import Functions


class CorrelationRes:
    def correlation(emo, name):

        price = []
        emotion = []
        with open('result\\' + name + '\\Csv_data\\'+name + ".csv", 'r') as G:
            # header row indexing with DictReader
            my_csv = csv.DictReader(G, delimiter=',')
            for row in my_csv:
                # print(row['price'])
                price.append(float(row['price']))
                # print(row[emo])
                emotion.append(int(row[emo]))
            # print(price)
            # print(emotion)

        correlate = pearsonr(price, emotion)
        return correlate[0]

    def correlation_csv(name):
        emotion_list = ["amusement", "interest", "pride", "joy", "pleasure", "relief", "compassion",
                        "admiration", "contentment", "love", "disappointment", "regret", "sadness",
                        "shame", "guilt", "hate", "contempt", "disgust", "fear", "anger"]

        test_file = open('result\\' + name + '\\Csv_data\\'+name + "_CT.csv", "w", newline='')
        f = csv.writer(test_file)

        count = 0
        if count == 0:
            # Headers
            f.writerow(emotion_list)
            count += 1

        row=[]
        for i in emotion_list:
            row.append(CorrelationRes.correlation(i,name))
        f.writerow(row)
        print(row)

CorrelationRes.correlation_csv("$AAPL")