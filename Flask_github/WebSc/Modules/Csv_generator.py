import csv
import json
from datetime import datetime
from pandas.io.data import DataReader
from Modules import Functions


class CsvGenerate:

    def get_price(company, year, month, day):
        try:
            face_book = DataReader(company, "yahoo", datetime(year, month, day), datetime(year, month, day))
            closing = face_book['Close']
            # print(closing[0])
            return closing[0]
        except BaseException as e:
            # print(0)
            return 0

    def create_csv(name):

        file_list = Functions.open_folder('result\\' + name + '\\')

        test_file = open('result\\' + name + '\\Csv_data\\'+name + ".csv", "w", newline='')
        f = csv.writer(test_file)

        emotion_list = ["time", "price", "amusement", "interest", "pride", "joy", "pleasure", "relief", "compassion",
                        "admiration", "contentment", "love", "disappointment", "regret", "sadness", "shame", "guilt", "hate",
                        "contempt", "disgust", "fear", "anger"]
        count = 0
        if count == 0:
            # Headers
            f.writerow(emotion_list)
            count += 1

        emotion_result = []
        for file in file_list:
            load = open(file, "r")
            loaded = json.load(load)
            emotion_result.append(loaded)

        for x in emotion_result:
            row = []
            for item in x:
                # add price and time first
                if "time" in item:
                    row.append(x["time"])
                    # print(x["time"])
                    d = datetime.strptime(x["time"], '%d-%m-%y')
                    month_ = d.strftime('%m').lstrip("0")
                    year_ = d.strftime('%Y')
                    day_ = d.strftime('%d')
                    comp = name.lstrip("$")
                    price = CsvGenerate.get_price(comp, int(year_), int(month_), int(day_))
                    row.append(price)
            for item in x:
                # add emotions
                if "emotions" in item:
                    # for all emotion strengths
                    for emo in x["emotions"]:
                        # print(emo)
                        for i in emotion_list:
                            if i is not "time" and i is not "price":
                                if i in emo:
                                    row.append(emo[i])
                                else:
                                    row.append(0)
            # print(row)
            f.writerow(row)

        test_file.close()
        print("done")

