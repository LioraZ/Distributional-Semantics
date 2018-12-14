import numpy as np
from collections import defaultdict, Counter
from itertools import islice
import pickle
import time
import sys
import pprint

DATA_FILE = "smaller"#"wikipedia.sample.trees.lemmatized" #"smaller"#
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

MIN_WORD_FREQUENCY = 100
MIN_FEATURE_FREQUENCY = 20
MIN_MUTUAL_FREQUENCY = 3

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
        #take only frequent words and attributes
        if word != occ_word and lemma_count[word] >= MIN_WORD_FREQUENCY and lemma_count[occ_word] >= MIN_FEATURE_FREQUENCY:
            word_count[word][occ_word] += 1
            word_count[word][OTHER] += 1
            word_count[OTHER][occ_word] += 1


def sentence_co_occurrence(sentence):
    content_words = [wtoi[word[LEMMA]] for word in sentence if word[POS_TAG] in CONTENT_POS_TAGS]
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


def get_op_direction( dir1):
    if dir1 == 'P':
        return 'C'
    else:
        return 'P'
        
        
def dependency_co_occurrence(sentence):
    #content_words = [word[LEMMA] for word in sentence if word[POS_TAG] in CONTENT_POS_TAGS]
    for a, b, word, word_tag, word_head, f in sentence: #content_words:
        word_index = wtoi[word]
    if lemma_count[word_index] >= MIN_WORD_FREQUENCY:
        if sentence[int(word_head)-1][POS_TAG] == "IN": # preposition
            attr_index_in_sen = int(sentence[int(word_head)-1][HEAD]) - 1
            attr_index = wtoi[sentence[attr_index_in_sen][LEMMA]]
            attr_pos = sentence[attr_index_in_sen][POS_TAG]
            direction = 'P'
        else:
            attr_index_in_sen = int(word_head) - 1 #sentence[int(word_head)-1]
            attr_index = wtoi[sentence[attr_index_in_sen][LEMMA]]
            attr_pos = sentence[attr_index_in_sen][POS_TAG]
            direction = 'C'
        if lemma_count[attr_index] >= MIN_FEATURE_FREQUENCY:
            word_count[word_index][(attr_index, direction, attr_pos)] += 1
            #attrs[(attr_index, direction, attr_pos)].add(word_index)
        if lemma_count[attr_index] >= MIN_WORD_FREQUENCY and  lemma_count[attr_index] >= MIN_FEATURE_FREQUENCY:
            word_count[attr_index][(word_index, get_op_direction(direction), word_tag)] += 1
            #attrs[(word_index, get_op_direction(direction), word_tag)].add(attr_index)



def read_data():
    start_time = time.time()
    global sentences, wtoi, itow, lemma_count
    #sentences = []
    sentence = []
    with open(DATA_FILE, encoding='utf8', mode='r') as file:
        for line in file:
            if line == '\n':
                #co_occurrence_type(sentence)
                sentences.append(sentence)
                sentence = []
            else:
                fields = line.split('\t')
                token = [fields[0], fields[1], fields[2], fields[3], int(fields[6]), fields[7]]
                sentence.append(token)
    curr_time = time.time()
    print("Creating count dictionary took:" + str(curr_time - start_time) + '\n')
    vocab = set([item for sublist in sentences for _, _, item, _, _, _ in sublist])
    wtoi = {word: i for i, word in enumerate(vocab)}
    itow = {i: word for i, word in enumerate(vocab)}
    #target_words = ["car", "bus", "hospital", "hotel", "gun", "bomb", "horse", "fox", "table", "bowl", "guitar", "piano"]
    lemma_count = Counter([wtoi[item] for sublist in sentences for _, _, item, _, _, _ in sublist])



def get_word_count(c_occ_func, sentences):
    for sen in sentences:
        c_occ_func(sen)

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
    sentences = []
    wtoi = defaultdict(int_default_dict)
    itow = defaultdict(int_default_dict)
    lemma_count = defaultdict(int_default_dict)
    #read_data(c_occ_func)
    read_data()
    get_word_count(c_occ_func, sentences)
    pickle.dump(word_count, open("word_counts_" + c_occ_type + ".save", "wb"))
    pickle.dump(wtoi,  open("word_to_index" + c_occ_type + ".save", "wb"))
    pickle.dump(itow,  open("index_to_word" + c_occ_type + ".save", "wb"))
    #pickle.dump(lemma_count,  open("lemma_count" + c_occ_type + ".save", "wb"))
    #for keys,values in word_count.items():
    #    print(itow[keys])
    #    print(values)
