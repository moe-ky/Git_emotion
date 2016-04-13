import collections
import glob
import json
import os
from Archive import twitterstreamV2
from Modules import Functions
import time


def num_of_tweets(name):
        # read in any json file that comes in/ using glob for filename pattern matching
    source = 'Tracker\\'+name
    json_dir = source
    json_pattern = os.path.join(json_dir, '*.json')
    file_list = glob.glob(json_pattern)

    for file in file_list:
        print(file)
        target_doc = open(file, 'r')
        sum_tweets = sum(1 for line in target_doc)
        print(sum_tweets)


# binary sorting
def alpha_words(name):
    # open dictionary
    source = 'Emotion\\'
    json_pattern = os.path.join(source, '*.json')
    file_list = glob.glob(json_pattern)

    # for each dictionary
    for file_emo in file_list:
        load_file = json.load(open(file_emo, 'r'))
        # print(load_file)
        # read in any json file that comes in/ using glob for filename pattern matching
        source = 'Tracker\\'+name
        json_pattern = os.path.join(source, '*.json')
        file_list = glob.glob(json_pattern)
        for file in file_list:
            # open each file in file list
            target_doc = open(file, 'r')
            Functions.num_of_tweets(file)

            res = []
            # for each line in document
            for lines in target_doc:
                word_list = []
                line = lines.lower()
                word = Functions.preprocess(line)
                for i in word:
                    # append to word list to be sorted
                    word_list.append(i)

                # sort each line in alphabetic order
                word_list.sort()
                #print(word_list)

                # check if the dictionary word is in the list
                dict_words = load_file["words"][0]
                if len(dict_words) == 0:
                    id_ = load_file["id"]
                    wrd = 0
                    di_ct = {id_: wrd}
                    res.append(di_ct)
                else:
                    for X in dict_words:
                        # print(X)
                        if Functions.binary_search(word_list, X) is True:
                            id_ = load_file["id"]
                            wrd = dict_words[X]
                            di_ct = {id_: wrd}
                            # print(di_ct)
                            res.append(di_ct)
                        else:
                            id_ = load_file["id"]
                            wrd = 0
                            di_ct = {id_: wrd}
                            res.append(di_ct)
        Functions.counting(res, file,"19-02-2016",200,name)


def emotion_measure(name):
    # read in any json file that comes in/ using glob for filename pattern matching
    source = 'Tracker\\'+name
    json_dir = source
    json_pattern = os.path.join(json_dir, '*.json')
    file_list = glob.glob(json_pattern)

    for file in file_list:

        print(file)
        target_doc = open(file, 'r')
        res = []
        time_stamp = Functions.time_stamp(file)
        num_tweets = Functions.num_of_tweets(file)
        Functions.num_of_tweets(file)
        for lines in target_doc:
            # print(lines)
            line = lines.lower()
            word = twitterstreamV2.preprocess(line)

            source = 'Emotion\\'
            json_dir = source
            json_pattern = os.path.join(json_dir, '*.json')
            file_list = glob.glob(json_pattern)

            for file_emo in file_list:
                emo_doc = open(file_emo, 'r')
                load_file = json.load(emo_doc)

                for wd in word:
                    # checks if the word exists in the dictionary and prints it out
                    dict_words = load_file["words"][0]
                    if wd in dict_words:
                        id_ = load_file["id"]
                        wrd = dict_words[wd]
                        di_ct = {id_: wrd}
                        res.append(di_ct)
                        #print(wd)
                        #print(di_ct)
                    else:
                        id_ = load_file["id"]
                        wrd = 0
                        di_ct = {id_: wrd}
                        res.append(di_ct)

        target_doc.close()
        #print(res)
        Functions.counting(res, file, time_stamp, num_tweets, name)
        # print(file)
        # results(res, file)


def results(res, source):
    file_source = source
    data = open('result.json', 'r')
    data_read = json.load(data)
    for item in res:
        for key in item:
            if key in data_read:
                data_read[key] += item[key]
            else:
                data_read[key] = item[key]
    # for key, value in sorted(data_read.items(), key=operator.itemgetter(1)):
    #    print(key, value)
    with open('result.json', 'w') as f:
        json.dump(data_read, f)
    # print("this is res after")
    print(data_read)

    destination = 'Historical\\'

   # shutil.move(file_source, destination)

t = time.time()
alpha_words("$AAPL")
elapsed = time.time() - t
print(elapsed)

'''
t = time.time()
emotion_measure("$AAPL")
elapsed = time.time() - t
print(elapsed)
'''