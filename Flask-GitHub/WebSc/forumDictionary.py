import json
import operator
import string

import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from Archive import twitterstreamV2

symbol = "aapl"
link = [
    'http://boards.fool.co.uk/is-it-me-or-is-a-recession-coming-13304214.aspx?sort=whole#13306203',
    'http://boards.fool.co.uk/globo-results-out-13205697.aspx?sort=whole#13307998',
    'http://boards.fool.co.uk/rbs-says-quotsell-everythingquot-13315850.aspx?sort=whole#13316150',
    'http://boards.fool.co.uk/stop-trying-to-time-the-market-13315511.aspx?sort=whole#13316307',
    'http://boards.fool.co.uk/gulf-markets-tumbling-9966814.aspx?sort=whole#9966863',
    'http://boards.fool.co.uk/sell-everything-ahead-of-cataclysmic-crisis-13316017.aspx?sort=whole#13316451',
    'http://boards.fool.co.uk/why-isnt-a-commodity-rout-a-good-thing--13315948.aspx?sort=whole#13316325'
]
punctuation = list(string.punctuation)
stop_words = stopwords.words('english') + punctuation + ['rt', 'via', 'ftse']

'''
symbols = ['.', "(", ")", ",", ":", "%", "'", "-", "i", "n't"]
for x in symbols:
    fulllist = stop_words.add(x)

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
    clean_up(word_list)

'''
split the words and remove unnecessary symbols
'''


def clean_up(word_list):
    clean_up_words = []
    for word in word_list:
        if word not in stop_words:
            # remove punctuation and replace with empty space
            punct = '1234567890'
            for i in range(0, len(punct)):
                word = word.replace(punct[i], "\n")
                word = word.replace("\n", "")
            if len(word) > 3:
                clean_up_words.append(word)
                #print(word)
    create_dictionary(clean_up_words)


'''
create a dictionary
'''


def create_dictionary(clean_up_word):
    data = {}
    for word in clean_up_word:
        if word in data:
            data[word] += 1
        else:
            data[word] = 1
        # sort dictionary by value
    for key, value in sorted(data.items(), key=operator.itemgetter(1)):
        if value > 20:
            print(key, value)
    with open('Emotion\\Words.json', 'w') as f:
        json.dump(data, f)


i = 0

while i < len(link):
    scrape(link[i])
    i += 1
