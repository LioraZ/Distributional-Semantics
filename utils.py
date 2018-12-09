import numpy as np
from collections import defaultdict
from itertools import islice
import pickle
import time
import sys

DATA_FILE = "wikipedia.sample.trees.lemmatized"
CONTENT_POS_TAGS = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN',
                    'VBP', 'VBZ', 'WRB']

ID = 0
FORM = 1
LEMMA = 2
POS_TAG = 3
HEAD = 4
DEPREL = 5

OTHER = "<other/>"
WINDOW_SIZE = 5

counter = 0


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def update_word_count(word, content_words):
    for occ_word in content_words:
        if word != occ_word:
            word_count[word][occ_word] += 1
            word_count[word][OTHER] += 1
            word_count[OTHER][occ_word] += 1


def sentence_co_occurrence(sentence):
    content_words = [word[LEMMA] for word in sentence if word[POS_TAG] in CONTENT_POS_TAGS]
    for word in content_words:
        update_word_count(word, content_words)


def window_co_occurrence(sentence):
    content_words = [word[LEMMA] for word in sentence if word[POS_TAG] in CONTENT_POS_TAGS]
    for i in range(len(content_words)):
        word = content_words[i]
        update_word_count(word, content_words[max(0, i - 2):i + 3])


def dependency_co_occurrence(sentence):
    print("hi")


def read_data(co_occurrence_type):
    start_time = time.time()
    sentence = []
    with open(DATA_FILE, encoding='utf8', mode='r') as file:
        for line in file:
            if line == '\n':
                co_occurrence_type(sentence)
                sentence = []
            else:
                fields = line.split('\t')
                token = [fields[0], fields[1], fields[2], fields[3], int(fields[6]), fields[7]]
                sentence.append(token)
    curr_time = time.time()
    print("Creating count dictionary took:" + str(curr_time - start_time) + '\n')


def int_default_dict():
    return defaultdict(int)


def get_co_occurrence_type():
    type = sys.argv[1]
    if type == 'sentence':
        return type, sentence_co_occurrence
    if type == 'window':
        return type, window_co_occurrence
    if type == 'dependency':
        return type, dependency_co_occurrence
    else:
        raise Exception("Illegal arguments exception!")


if __name__ == '__main__':
    c_occ_type, c_occ_func = get_co_occurrence_type()
    word_count = defaultdict(int_default_dict)
    read_data(c_occ_func)
    pickle.dump(word_count, open("word_counts_" + c_occ_type + ".save", "wb"))

