from Modules import Functions
import string
import unittest
from nltk.util import bigrams
import json
import networkx as nx
from networkx.readwrite import json_graph
import os
import csv
from datetime import datetime
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")
punctuation = list(string.punctuation)
negation_list = ["never", "not", "dont"]
intensifier_list = ["extremely", "very"]


class Company:

    def __init__(self, name):
        self.name = name
        self.dictionary = "C:/Users/MOYIN/Desktop/Flask/WebSc/Emotion_Dictionary.json"
        self.groups = "C:/Users/MOYIN/Desktop/Flask/WebSc/Emotion_Groups.json"

    def run(self):
        Company.data_collection(self)

    def data_collection(self):

        try:

            name = self.name
            path = "Tracker\\" + name
            file_list = Functions.open_folder(name, path)
            if file_list:
                Company.pre_process(self,file_list)
            else:
                Functions.get_data(name,path)
                Company.data_collection(self)
            # print(file_list)
            return file_list

        except BaseException as e:

            print("data collection error: ", e)

    def pre_process(self, file_list):

        try:
            print(file_list)
            x=0
            while x < len(file_list):
                num_tweets = Functions.num_of_tweets(file_list[x])
                # print(num_tweets)
                target_doc = open(file_list[x], 'r')
                time_stamp = Functions.time_stamp(file_list[x])
                # print(time_stamp)
                # print(file_list[x])
                target_doc = open(file_list[x], 'r')
                # print(target_doc)
                for lines in target_doc:
                        word_list =[]
                        line = lines.lower()
                        word = Functions.preprocess(line)
                        for i in word:
                            if i not in punctuation:
                                word_list.append(i)
                    # print(word_list)
                        Company.emotion_analysis(self,word_list,file_list[x],time_stamp,num_tweets)
                x += 1
                return word_list
        except BaseException as e:

                print("Pre_process error: ", e)

    def emotion_analysis(self,word_list,file,time_stamp,num_tweets):

        try:

            negation_counter = 0
            res = []
            name = self.name

            # open dictionary and order words alphabetically
            dict_file = self.dictionary
            dictionary = open(dict_file, "r")
            di_ct = json.load(dictionary)
            ordered = Functions.word_order(di_ct)

            grams = list(bigrams(word_list))
            negative_flag = False
            intensifier_flag = False
            # print(word_list)
            for x in word_list:
                # perform matching of words in word_list with words in dictionary
                x_stemmed = stemmer.stem(x)
                if Functions.binary_search(self, ordered, x) is True:
                    # use bigrams to determine negation and intensifiers
                    for i in grams:
                        if x in i:
                            # check for negation
                            for n in negation_list:
                                if n not in i:
                                    pass
                                else:
                                    negative_flag = True
                            # check for intensifier
                            for n in intensifier_list:
                                if n not in i:
                                    pass
                                else:
                                    # print(i)
                                    intensifier_flag = True
                    # handles negation and intensifier occurrence
                    if negative_flag is True:
                        negation_counter += 1
                        negative_flag = False
                    else:
                        if di_ct[x]:
                            i_d = di_ct[x][1]
                            if intensifier_flag is True:
                                wrd = di_ct[x][0] + 2
                                intensifier_flag = False
                            else:
                                wrd = di_ct[x][0]
                            new_d = {i_d: abs(wrd)}
                            res.append(new_d)
                else:
                    pass
            #print("negation count :", negation_counter)
            #print(negative_flag)
            # print("number of tweets :" , num_tweets)
            Functions.counting(self, res, file, time_stamp, num_tweets,name)
            # Company.create_graph(self,name)
            # Company.create_csv(self, name)
            # dictionary.close()
            return res

        except BaseException as e:

            print ("emotion analysis error: ", e)

    def create_graph(self,name):

        try:

            groups = open(self.groups, "r")
            load_groups = json.load(groups)
            G = nx.Graph()

            file_list = Functions.open_folder(name,'C:/Users/MOYIN/Desktop/Flask/WebSc/result/' + name + '/')

            for file in file_list:
                load = open(file, "r")
                result_json = json.load(load)

                G.add_node("Emotion", x=500, y=400, fixed=True)
                for wd in result_json['emotions']:
                    for word in wd:
                        G.add_node(word, group=load_groups[word])
                        G.add_edge("Emotion", word, value=wd[word])
                d = json_graph.node_link_data(G)

                # file = open("result\\" + self + "\\Force_layout\\" + os.path.basename(file), 'w')
                filex = open("C:/Users/MOYIN/Desktop/Flask/static/Companies/" + name + "/"+os.path.basename(file), 'w')
                json.dump(d, filex)
                filex.close()
                #print("Graph files created")
                return os.path.basename(file)
            groups.close()

        except BaseException as e:
            print ("Graph creation error : ", e)

    def create_csv(self,name):

        try:

            file_list = Functions.open_folder(self, 'result\\' + name + '\\')

            test_file = open('C:/Users/MOYIN/Desktop/Flask/WebSc/result/' + name + '/Csv_data/'+name + ".csv", "w",
                             newline='')
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
                        price = Functions.get_price(comp, int(year_), int(month_), int(day_))
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
            #print("CSV file generated")
            Company.correlation_csv(self,name)
            return test_file.name

        except BaseException as e:
            print ("Create csv error: ", e)

    def correlation_csv(self,name):

        try:

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
                    row.append(Functions.correlation(i, name))
                    # print(row)
                    f.writerow(row)
                # print("correlation table created")
                test_file.close()
                return test_file.name

        except BaseException as e:
            print ("Correlation error : ", e)


class MyTest(unittest.TestCase):

    def test1(self):
        self.assertEqual(Company("$AAPL").data_collection(),['Tracker\\$AAPL\\$AAPL-16-03-16.json'])

    def test2(self):
        self.assertEqual(Company("$AAPL").pre_process(['Tracker\\$AAPL\\$AAPL-16-03-16.json']),["i", "am", "happy",'i', 'am', 'sad'])

    def test3(self):
        self.assertEqual(Company("$AAPL").emotion_analysis(["i", "am", "happy",'i', 'am', 'sad'],'Tracker\\$AAPL\\$AAPL16-03-16.json',"16-03-16",2),
                          [{'contentment': 2}, {'sadness': 2}])

    def test4(self):
        self.assertEqual(Company("$AAPL").create_graph("$AAPL"),"result_$AAPL-16-03-16.json")

    def test5(self):
        self.assertEqual(Company("$AAPL").create_csv("$AAPL"),"C:/Users/MOYIN/Desktop/Flask/WebSc/result/$AAPL/Csv_data/$AAPL.csv")

    def test6(self):
        self.assertEqual(Company("$AAPL").correlation_csv("$AAPL"),"C:/Users/MOYIN/Desktop/Flask/static/Companies/$AAPL/$AAPL_CT.csv")


unittest.main()
'''
apple = Company("$AAPL")
apple.data_collection()
'''