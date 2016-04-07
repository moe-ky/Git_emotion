import collections
import glob
import json
import os

from Archive import twitterstreamV2


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
        for lines in target_doc:

            line = lines.lower()
            word = twitterstreamV2.preprocess(line)
            i = 0

            docs = ['Emotion\\Angry.json', 'Emotion\\Fear.json', 'Emotion\\Hate.json', 'Emotion\\Disappointment.json',
                    'Emotion\\Pride.json', 'Emotion\\Contentment.json', 'Emotion\\interest.json',
                    'Emotion\\Amusement.json', 'Emotion\\Contempt.json', 'Emotion\\Disgust.json']

            while i < len(docs):

                '''
                source = 'Emotion\\'
                json_dir = source
                json_pattern = os.path.join(json_dir, '*.json')
                file_list = glob.glob(json_pattern)
                for file_emo in file_list:
                #print(file_emo)
                emo_doc = open(file_emo, 'r')
                load_file = json.load(emo_doc)
                '''
                emo_doc = open(docs[i], 'r')
                load_file = json.load(emo_doc)
                for wd in word:
                    # checks if the word exists in the dictionary and prints it out
                    dict_words = load_file["Words"][0]
                    if wd in dict_words:
                        id_ = load_file["ID"]
                        wrd = dict_words[wd]
                        di_ct = {id_: wrd}
                        print(di_ct)
                        res.append(di_ct)
                i += 1
        target_doc.close()
        # print(res)
        counting(res, file)
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


def counting(res, source):
    # counts the items in dict and sums them up
    counter = collections.Counter()
    for d in res:
        counter.update(d)
    counter = dict(counter)
    # create a new file with an extension of the files name for transparency
    with open('result\\result_' + os.path.basename(source), 'w') as f:
        json.dump(counter, f)

    print("final result")
    print(counter)

emotion_measure('$AAPL')

