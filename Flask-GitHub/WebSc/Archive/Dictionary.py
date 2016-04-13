from bs4 import BeautifulSoup
import requests
import operator
import io
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

symbol = "aapl"
link = 'http://boards.fool.co.uk/is-it-me-or-is-a-recession-coming-13304214.aspx?sort=whole#13306203'

stop_words = set(stopwords.words('english'))
symbols = ['.', "(", ")", ",", ":", "%", "'", "-", "i", "n't"]
for x in symbols:
    fulllist = stop_words.add(x)

'''
retrieve data in text format and split it to a list of words using word_tokenize
'''


def scrape(url):
    word_list = []
    req = requests.get(url).text
    soups = BeautifulSoup(req, "html.parser")
    block = soups.find_all('blockquote', {'class': 'pbmsg'})
    for block_text in block:
        content = block_text.text
        words = content.lower()
        for i in word_tokenize(words):
            word_list.append(i)
            print(i)
    clean_up(word_list)
'''
    for block_text in block:
        content = block_text.text
        # makes everything lowercase and splits words
        words = content.lower().split()
        for each_word in words:
            word_list.append(each_word)
    clean_up(word_list)
'''

'''
split the words and remove unnecessary symbols
'''


def clean_up(word_list):
    clean_up_words = []
    for word in word_list:
        if word not in stop_words:
            punct = '(),.<>/!"?1234567890%-&=_:\^";`$&*£“\''
            for i in range(0, len(punct)):
                word = word.replace(punct[i], "\n")
                word = word.replace("\n", "")
            if len(word) > 3:
                # print(word)
                clean_up_words.append(word)
    create_dictionary(clean_up_words)

'''
def clean_up(word_list):
    clean_up_words = []
    for word in word_list:
        symbols = '(),.<>/!"?1234567890%-&=_:\^"'
        for i in range(0, len(symbols)):
            word = word.replace(symbols[i], "")
        if len(word) > 0:
            #print(word)
            clean_up_words.append(word)
    create_dictionary(clean_up_words)
'''


def create_dictionary(clean_up_word):
    word_count = {}
    for word in clean_up_word:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    for key, value in sorted(word_count.items(), key=operator.itemgetter(1)):
        print(key, value)

scrape(link)

'''
with io.open('log.txt', 'w', encoding='utf8') as logfile:
    block = soups.find_all("blockquote", {"class": "pbmsg"})
    for item in block:
        print item.contents
        logfile.write(item.text)
'''
