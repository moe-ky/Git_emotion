import json
import operator
import string
from nltk.corpus import stopwords
from Modules import Functions

Docs = ['twitDB2.txt', 'twitDB3.txt']

punctuation = list(string.punctuation)
stop_words = stopwords.words('english') + punctuation + ['rt', 'via']


def convert():
    wordlist = []
    with open('tweets.json', 'r') as f:
        for line in f:
            # converts al lines to lowercase
            line = line.lower()
            # checks that line is not a new line
            if line != '\n':
                data = json.loads(line)
                # to solve keyError issue
                if 'text' in data:
                    if data["lang"] == "en" or data["lang"] == "en-gb":
                        text_data = data['text']
                        #print(text_data)
                        words = Functions.preprocess(text_data)
                        for word in words:
                            wordlist.append(word)
                            #print(word)
    clean_up(wordlist)


def scrape(file):
    with open(file, 'r') as f:
        wordlist = []
        for line in f:
            line = line.lower()
            tweet = Functions.preprocess(line)
            for i in tweet:
                wordlist.append(i)
        clean_up(wordlist)


def clean_up(word_list):
    clean_up_words = []
    for word in word_list:
        if word not in stop_words and not word.startswith(('#', '@')):
            # remove punctuation and replace with empty space
            '''
            punct = '1234567890'
            for i in range(0, len(punct)):
                word = word.replace(punct[i], "\n")
                word = word.replace("\n", "")
            '''
            if len(word) > 3:
                clean_up_words.append(word)
            #print(word)
    create_dictionary(clean_up_words)


def create_dictionary(clean_up_word):
    data = open('Emotion\\Tweet.json', 'r')
    data_read_ = json.load(data)
    data_read = {}
    for word in clean_up_word:
        if word in data_read:
            data_read[word] += 1
        else:
            data_read[word] = 1
        # sort dictionary by value
    for key, value in sorted(data_read.items(), key=operator.itemgetter(1)):
        if value > 200:
            print(key, value)
    with open('Emotion\\Tweet.json', 'w') as f:
        json.dump(data_read, f)


def collect_user():
    user = input("enter number here", )
    collect(int(user))
    return user


def collect(user):
    file_list = Functions.open_folder("","Lexicon_data\\")
    if user > len(file_list):
        pass
    else:
        num = int(user)
        print("Now analysing ", file_list[num], "--------------------------------")
        scrape(file_list[num])
        collect_user()

convert()
#collect_user()