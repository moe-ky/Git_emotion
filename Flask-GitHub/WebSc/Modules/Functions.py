import collections
import os
import re
import json
import glob
from Modules import TwitterCatch
from pandas.io.data import DataReader
from scipy.stats.stats import pearsonr
from datetime import datetime
import csv


# function to pre process text files
# ---------------- pre-process list of words ----------------
# Source http://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/
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
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


# ---------------------------- Function carries out binary search
# Source : http://interactivepython.org/runestone/static/pythonds/SortSearch/TheBinarySearch.html
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


def reduce(self, res, source, time_stamp, num_tweets, name):
# counts the items in dict and sums them up
    counter = collections.Counter()
    for d in res:
        counter.update(d)
    counter = dict(counter)
    # create a new file with an extension of the files name for transparency
    with open('C:/Users/MOYIN/Desktop/Flask/WebSc/result/' + name+'/result_' + os.path.basename(source), 'w') as f:
        count = []
        count.append(counter)
        result = {"time": time_stamp, "emotions": count, "Tweet count": num_tweets}
        json.dump(result, f, sort_keys=True)
    print(result)

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


def open_folder(name, path):
    source = path
    json_pattern = os.path.join(source, '*.json')
    file_list = glob.glob(json_pattern)
    if file_list:
        return file_list

# ---------------------------- gets data from twitter


def get_data(name,path):
    print("fetching files")
    TwitterCatch.catch(name)
    open_folder(name, path)

# ---------------------------- gets price data


def get_price(company, year, month, day):
    try:
        face_book = DataReader(company, "yahoo", datetime(year, month, day), datetime(year, month, day))
        closing = face_book['Close']
        # print(closing[0])
        return closing[0]
    except BaseException as e:
        # print(0)
        return 0

# ---------------------------- calculates correlation


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