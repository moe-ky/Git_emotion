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
negation_counter = 0


class Company:

    def __init__(self, name):
        self.name = name
        self.dictionary = "C:/Users/MOYIN/Desktop/Flask/WebSc/Dictionary/extended_dict.json"
        self.groups = "C:/Users/MOYIN/Desktop/Flask/WebSc/Emotion_Groups.json"

    def data_collection(self):

        try:

            name = self.name
            path = "C:/Users/MOYIN/Desktop/Flask/WebSc/Tracker/" + name
            # get all files in folder
            file_list = Functions.open_folder(name, path)
            # check if files exists
            if file_list:
                Company.pre_process(self,file_list)
            else:
                Functions.get_data(name,path)
                Company.data_collection(self)
            return file_list

        except BaseException as e:

            print("data collection error: ", e)

    def pre_process(self, file_list):

        try:
            # Split text into a list of words
            list_ = []
            x = 0
            while x < len(file_list):
                num_tweets = Functions.num_of_tweets(file_list[x])
                time_stamp = Functions.time_stamp(file_list[x])
                target_doc = open(file_list[x], 'r')
                print("FILE: ",target_doc.name)
                res = []
                for lines in target_doc:
                    word_list = []
                    line = lines.lower()
                    word = Functions.preprocess(line)
                    for i in word:
                        if i not in punctuation:
                            word_list.append(i)
                            # For testing purposes
                            list_.append(i)
                    Company.emotion_analysis(self,word_list,file_list[x],time_stamp,num_tweets,res)
                x += 1
            # print(list_)

            return list_
        except BaseException as e:

                print("Pre_process error: ", e)

    def emotion_analysis(self,word_list,file,time_stamp,num_tweets,res):

        try:
            name = self.name
            # open dictionary and order words alphabetically
            dict_file = self.dictionary
            dictionary = open(dict_file, "r")
            di_ct = json.load(dictionary)
            ordered = Functions.word_order(di_ct)

            # obtain bigrams for detecting negation
            grams = list(bigrams(word_list))
            negative_flag = False
            intensifier_flag = False
            intensi = []
            negate = []
            # check for negating of intensifier words
            for i in grams:
                for n in negation_list:
                    if n in i:
                        negate.append(i)
                        negative_flag = True
                for n in intensifier_list:
                    if n in i:
                        intensi.append(i)
                        intensifier_flag =True
            # print(word_list)

            for x in word_list:
                if Functions.binary_search(self, ordered, x) is True:
                    if negative_flag is True:
                        for i in negate:
                            if x in i:
                                pass
                        pass
                    else:
                        wrd =0
                        if di_ct[x]:
                            i_d = di_ct[x][1]
                            if intensifier_flag is True:
                                for i in intensi:
                                    if x in i:
                                        wrd = di_ct[x][0] + 1
                                        intensifier_flag = False
                                    else:
                                        wrd = di_ct[x][0]
                            else:
                                wrd = di_ct[x][0]
                            new_d = {i_d: abs(wrd)}
                            res.append(new_d)
                # accommodate for stemmed words, future development -------------------
                elif Functions.binary_search(self,ordered,stemmer.stem(x))is True:
                    x_stem = stemmer.stem(x)
                    # handles negation and intensifier occurrence
                    if negative_flag is True:
                        # negation_counter += 1
                        pass
                    else:
                        if di_ct[x_stem]:
                            # print(x)
                            i_d = di_ct[x_stem][1]
                            if intensifier_flag is True:
                                wrd = di_ct[x_stem][0] + 1
                                intensifier_flag = False
                            else:
                                wrd = di_ct[x_stem][0]
                            new_d = {i_d: abs(wrd)}
                            res.append(new_d)
                            # print(new_d)
            Functions.reduce(self, res, file, time_stamp, num_tweets,name)
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
            print(file_list)

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
                print("Graph files created: ", filex.name)
            return os.path.basename(file)

        except BaseException as e:
            print ("Graph creation error : ", e)

    def create_csv(self,name):

        try:

            file_list = Functions.open_folder(self, 'C:/Users/MOYIN/Desktop/Flask/WebSc/result/' + name + '/')

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

            for file in file_list:
                emotion_result = []
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
                    #print(row)
                    f.writerow(row)
            print("CSV file generated : ")
            #Company.correlation_csv(self,name)
            return test_file.name

        except BaseException as e:
            print("Create csv error: ", e)

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
                    correlate = Functions.correlation(i, name)
                    row.append(correlate)
                    print(row)
                    f.writerow(row)
                print("correlation table created")
                print("----------------------------------------------------------------")
                test_file.close()
                return test_file.name

        except BaseException as e:
            print("Correlation error : ", e)