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
DEP_REL = 5

OTHER = "<other/>"
UP = "<up/>"
DOWN = "<down/>"
WINDOW_SIZE = 5


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


def get_dependency_tree(sentence):
    parents = defaultdict(list)
    children = defaultdict(list)
    for word in sentence:
        parent = word[HEAD]
        #children[parent] += [word]
        parents[word[ID]] += [parent]

    for p_id in parents.keys():
        parent = sentence[p_id - 1]
        parent_change = []
        while parent[POS_TAG] not in CONTENT_POS_TAGS and parent not in 'IN':
            parent_change.append(parent)
            parent = parents[parent[ID]]
            if parent == 0:
                break
#        p[]
        """for p in parent_change:
            parents[p] = parent"""

    #children = {c: p_id for p_id in parents for c in parents[p_id]}
    for p_id in parents:
        for c in parents[p_id]:
            children[c] += [p_id]

    return parents, children




def dependency_co_occurrence(sentence):
    parents, children = get_dependency_tree(sentence)
    """for p_id in parents:

   for word in sentence:
        parent_id = word[HEAD]
        if parent_id == 0:
            continue
        if word[POS_TAG] == 'IN':
            raise NotImplemented
        else:
            parent = sentence[parent_id - 1]
            word_count[word[LEMMA]][parent[LEMMA] + '\t' + word[DEP_REL] + '\t' + UP] += 1
            word_count[parent[LEMMA]][word[LEMMA] + '\t' + word[DEP_REL] + '\t' + DOWN] += 1

            word_count[word[LEMMA]][OTHER] += 1
            word_count[parent[LEMMA]][OTHER] += 1
            word_count[OTHER][word[LEMMA]] += 1
            word_count[OTHER][parent[LEMMA]] += 1"""


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

