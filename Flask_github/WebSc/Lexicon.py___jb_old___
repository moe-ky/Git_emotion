from textblob import Word
from textblob.wordnet import Synset
from nltk.parse import stanford
import csv
import json
from Modules import Functions
from nltk.stem.snowball import SnowballStemmer

'''
word = Word("good").get_synsets(pos=NOUN)
chosen = word[1].lemma_names()
print(chosen)
'''

stemmer = SnowballStemmer("english")

dict_file = "C:/Users/MOYIN/Desktop/Flask/WebSc/Emotion_Dictionary_ORG.json"
dictionary = open(dict_file, "r")
di_ct = json.load(dictionary)
ordered = Functions.word_order(di_ct)
words = ordered

'''
for i in di_ct:
    print(di_ct[i])
'''

# source: https://gist.github.com/cdtavijit/431135aa6da53d47bc72


def synonym_finder(specific_word, synonymList):
    word = Word(specific_word)
    for i,j in enumerate(word.synsets):
        # print "Synonyms:", ", ".join(j.lemma_names())
        for x in range (len(j.lemma_names())):
            if j.lemma_names()[x] not in synonymList:
                synonymList.append(str(j.lemma_names()[x]))
# -------------------------------------------------------------


def extend(word_list):
    for word in word_list:
        newlist = []
        new_D_list = {}
        syn = []
        synonym_finder(word,syn)
        for s in syn:
            if s not in newlist:
                newlist.append(s)

            new_entry = {word:newlist}
            new_D_list.update(new_entry)
        print(new_D_list)

        with open("newDict.json", 'a') as newF:
            json.dump(new_D_list,newF)
            newF.write(","+"\n"+"\n")


file = "newDict.json"
open_file = open("newDict.json", 'r')
di_cts = json.load(open_file)
# print(di_cts)
extended_word_list ={}
for words in di_cts:
    for i in words:
        info = di_ct[i]
        new_ent = {i:info}
        extended_word_list.update(new_ent)
        for x in words[i]:
            new_ents = {x:info}
            extended_word_list.update(new_ents)
with open("extended_dict.json", "w") as ext:
    json.dump(extended_word_list, ext)
    print("done")


'''
extended from 87 words to 388 words
count = 0
for i in extended_word_list:
    print(i, count)
    count += 1
print(count)
'''
