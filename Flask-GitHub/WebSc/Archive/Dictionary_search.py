import string
from nltk.corpus import stopwords
import collections
import re
import glob
import networkx as nx
from networkx.readwrite import json_graph
import os
import json
from datetime import datetime
from pandas.io.data import DataReader
from scipy.stats.stats import pearsonr
import csv
import time
import nltk
from nltk.util import bigrams

punctuation = list(string.punctuation)
stop_words = stopwords.words('english') + punctuation + ['rt', 'via']

negation_list = ["never", "not", "dont"]
intensifier_list = ["extremely", "very"]


def data_collection(name):
    path = "Tracker\\" + name
    Functions.open_folder(path)


class Search:

    def __init__(self, name):
        self.name = name
        self.dictionary = "C:/Users/MOYIN/Desktop/Flask/WebSc/Emotion_Dictionary.json"

    def company(self):
        name = self.name
        dict_file = self.dictionary
        dictionary = open(dict_file, "r")
        di_ct = json.load(dictionary)
        ordered = Functions.word_order(di_ct)

        file_list = Functions.open_folder('Tracker\\' + name)
        if file_list:
            for file in file_list:
                # open each file in file list
                target_doc = open(file, 'r')
                # time stamp
                time_stamp = Functions.time_stamp(file)
                # number of tweets
                num_tweets = Functions.num_of_tweets(file)

                res = []
                word_list = []
                negation_counter = 0
                # for each line in document
                for lines in target_doc:
                    line = lines.lower()
                    word = PreProcess.preprocess(line)
                    for i in word:
                        if i not in punctuation:
                            word_list.append(i)

                grams = list(bigrams(word_list))
                negative_flag = False
                intensifier_flag = False
                #print(word_list)
                for x in word_list:
                    if Functions.binary_search(self, ordered, x) is True:
                        for i in grams:
                            if x in i:
                                for n in negation_list:
                                    if n not in i:
                                        pass
                                    else:
                                        # print(i)
                                        negative_flag = True
                                for n in intensifier_list:
                                    if n not in i:
                                        pass
                                    else:
                                        # print(i)
                                        intensifier_flag = True

                        if negative_flag is True:
                            negation_counter += 1
                            negative_flag = False
                        else:
                            i_d = di_ct[x][1]
                            if intensifier_flag is True:
                                wrd = di_ct[x][0] + 2
                                intensifier_flag = False
                            else:
                                wrd = di_ct[x][0]
                            new_d = {i_d: abs(wrd)}
                            # print(new_d)
                            res.append(new_d)
                    else:
                        pass
                print("negation count :", negation_counter)
                print("number of tweets :" , num_tweets)
                Functions.counting(self, res, file, time_stamp, num_tweets, name)
        else:
            print ("no files found")

        Graph.create_graph(name)
        CsvGenerate.create_csv(name)
        CorrelationRes.correlation_csv(name)


class Functions(Search):

    def __init__(self, a_list):
        self.a_list = a_list

    # ---------------------------- Function carries out binary search
    def binary_search(self, a_list, item):

        first = 0
        last = len(a_list)-1
        found = False

        while first <= last and not found:
            midpoint = (first + last)//2
            if a_list[midpoint] == item:
                found = True
            else:
                if item < a_list[midpoint]:
                    last = midpoint-1
                else:
                    first = midpoint+1
        return found

    # ----------------------------  Function carries out emotion analysis result counting and formatting
    def counting(self, res, source, time_stamp, num_tweets, name):
        # counts the items in dict and sums them up
        counter = collections.Counter()
        for d in res:
            counter.update(d)
        counter = dict(counter)
        # create a new file with an extension of the files name for transparency
        with open('result\\' + name+'\\result_' + os.path.basename(source), 'w') as f:
            count = []
            count.append(counter)
            result = {"time": time_stamp, "emotions": count, "Tweet count": num_tweets}
            json.dump(result, f, sort_keys=True)
        # print(result)

    # ---------------------------- separates key from dictionary and orders it
    def word_order(di_ct):
            worded = []
            for key in di_ct:
                key = key.lower()
                worded.append(key)
            ordered = sorted(worded)
            return ordered

    # ---------------------------- Get the number of tweets in a file
    def num_of_tweets(file):
        count = 0
        with open(file, 'rb') as f:
            for line in f:
                count += 1
        return count

    # ---------------------------- Gets the time stamp in the file name
    def time_stamp(file):
        with open(file, 'r') as f:
            search_string = "([0-9]{2}\-[0-9]{2}\-[0-9]{2})"
            search = re.search(search_string, f.name)

            if search:
                return search.group(0)

    # ---------------------------- Opens folder and searches for json files
    def open_folder(path):
        source = path
        json_pattern = os.path.join(source, '*.json')
        file_list = glob.glob(json_pattern)
        return file_list


class PreProcess(Functions):
    # function to pre process text files
    # ---------------- pre-process list of words ----------------
    # SOURCE : http://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/
    emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""
    regex_str = [
        emoticons_str,
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
    ]
    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

    def tokenize(s):
        return PreProcess.tokens_re.findall(s)

    def preprocess(s, lowercase=False):
        tokens = PreProcess.tokenize(s)
        if lowercase:
            tokens = [token if PreProcess.emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens


class Graph(Search):

    def create_graph(self):

        groups = open("C:/Users/MOYIN/Desktop/Flask/WebSc/Emotion_Groups.json", "r")
        # connected = open("connected.json", "r")
        load_groups = json.load(groups)
        # load_connect = json.load(connected)

        G = nx.Graph()

        file_list = Functions.open_folder('C:/Users/MOYIN/Desktop/Flask/WebSc/result/result/' + self + '/')
        for file in file_list:
            load = open(file, "r")
            result_json = json.load(load)
            # print(os.path.basename(file))

            G.add_node("Emotion", x=500, y=400, fixed=True)
            for wd in result_json['emotions']:
                for word in wd:
                    # G.add_node(word, group=load_groups[word], x=200, y=300, fixed=True)
                    G.add_node(word, group=load_groups[word])
                    G.add_edge("Emotion", word, value=wd[word])

            d = json_graph.node_link_data(G)
            # file = open("result\\" + self + "\\Force_layout\\" + os.path.basename(file), 'w')
            file = open("C:/Users/MOYIN/Desktop/Flask/static/Companies/" + self + "/"+os.path.basename(file), 'w')
            # print(file)
            json.dump(d, file)
        print("Graph files created")


class CsvGenerate(Search):

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

        test_file = open('C:/Users/MOYIN/Desktop/Flask/WebSc/result/' + name + '/Csv_data/'+name + ".csv", "w", newline='')
        f = csv.writer(test_file)

        emotion_list = ["time", "price", "amusement", "interest", "pride", "joy", "pleasure", "relief", "compassion",
                        "admiration", "contentment", "love", "disappointment", "regret", "sadness", "shame", "guilt",
                        "hate","contempt", "disgust", "fear", "anger"]
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
                        for i in emotion_list:
                            if i is not "time" and i is not "price":
                                if i in emo:
                                    row.append(emo[i])
                                else:
                                    row.append(0)
            f.writerow(row)
        test_file.close()
        print("CSV file generated")


class CorrelationRes(Graph):
    def correlation(emo, name):
        price = []
        emotion = []
        with open('C:/Users/MOYIN/Desktop/Flask/WebSc/result/' + name + '/Csv_data/'+name + ".csv", 'r') as G:
            # header row indexing with DictReader
            my_csv = csv.DictReader(G, delimiter=',')
            for row in my_csv:
                price.append(float(row['price']))
                emotion.append(int(row[emo]))

        correlate = pearsonr(price, emotion)
        if str(correlate[0]) == "nan":
            return 0
        else:
            return correlate[0]

    def correlation_csv(name):
        emotion_list = ["amusement", "interest", "pride", "joy", "pleasure", "relief", "compassion",
                        "admiration", "contentment", "love", "disappointment", "regret", "sadness",
                        "shame", "guilt", "hate", "contempt", "disgust", "fear", "anger"]

        test_file = open("C:/Users/MOYIN/Desktop/Flask/static/Companies/"+name+"/"+name + "_CT.csv", "w+", newline='')
        test_file.truncate()
        f = csv.writer(test_file)

        count = 0
        if count == 0:
            # Headers
            headers = ["emotion", "correlation"]
            f.writerow(headers)
            count += 1

            for i in emotion_list:
                row=[]
                row.append(i)
                row.append(CorrelationRes.correlation(i, name))
                # print(row)
                f.writerow(row)
            print("correlation table created")


apple = Search("$AAPL")
apple.company()