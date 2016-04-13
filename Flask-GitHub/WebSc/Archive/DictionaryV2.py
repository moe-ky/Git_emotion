import json
import operator

import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from Archive import twitterstreamV2

symbol = "aapl"
link = 'http://boards.fool.co.uk/is-it-me-or-is-a-recession-coming-13304214.aspx?sort=whole#13306203'
# link = 'http://boards.fool.co.uk/globo-results-out-13205697.aspx?sort=whole#13307998'

stop_words = set(stopwords.words('english'))
symbols = ['.', "(", ")", ",", ":", "%", "'", "-", "i", "n't"]

for x in symbols:
    fulllist = stop_words.add(x)

'''
retrieve data in text format and split it to a list of words using regex from twitterstreamV2
'''



def scrape(url):
    word_list = []
    req = requests.get(url).text
    soups = BeautifulSoup(req, "html.parser")
    block = soups.find_all('blockquote', {'class': 'pbmsg'})
    for block_text in block:
        content = block_text.text
        words = content.lower()
        for i in twitterstreamV2.preprocess(words):
            word_list.append(i)
            # print (i)
    clean_up(word_list)

'''
split the words and remove unnecessary symbols
'''


def clean_up(word_list):
    clean_up_words = []
    for word in word_list:
        if word not in stop_words:
            # remove punctuation and replace with empty space
            punct = '(),.<>/!"?1234567890%-&=_:+@~|\^"”;`$&*£“\''
            for i in range(0, len(punct)):
                word = word.replace(punct[i], "\n")
                word = word.replace("\n", "")
            if len(word) > 3:
                # print(word)
                clean_up_words.append(word)
    create_dictionary(clean_up_words)


'''
create a dictionary
'''


def create_dictionary(clean_up_word):
    f = open('Emotion\\Words.json', 'r')
    data = json.load(f)
    for word in clean_up_word:
        if word in data:
            data[word] += 1
        else:
            data[word] = 1
        # sort dictionary by value
    for key, value in sorted(data.items(), key=operator.itemgetter(1)):
        print(key, value)
    with open('Emotion\\Words.json', 'w') as f:
        json.dump(data, f)

scrape(link)
