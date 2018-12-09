from collections import defaultdict
import pickle
import math
import sys

TARGET_WORDS = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']
OTHER = "<other/>"
THRESHOLD = 100


def PMI(word, attr):
    p_word = word_count[word][OTHER] / total_counts
    p_attr = word_count[OTHER][attr] / total_counts
    p_word_and_attr = word_count[word][attr] / total_counts

    p_word_mul_attr = p_word * p_attr
    if p_word_mul_attr == 0:
        return 0
    prob = p_word_and_attr / p_word_mul_attr
    if prob == 0:
        return 0
    return math.log(prob)


def get_total_count():
    return sum(word_count[word][OTHER] for word in word_count.keys() if word != OTHER)


def create_PMI_from_counts():
    counter = 0
    for word, attributes in word_count.items():
        counter += 1
        print(str(counter) + '\t' + word)

        if word_count[word][OTHER] < THRESHOLD or word == OTHER:
            continue
        for attribute in attributes:
            if word_count[OTHER][attribute] < THRESHOLD or attribute == OTHER:
                continue
            PMI_dict[word][attribute] = PMI(word, attribute)
            PMI_dict[word][OTHER] += PMI_dict[word][attribute] ** 2
            inv_PMI[attribute][word] = PMI(attribute, word)


def int_default_dict():
    return defaultdict(int)


def get_co_occurrence_type():
    type = sys.argv[1]
    if type == 'sentence':
        return type
    if type == 'window':
        return type
    if type == 'dependency':
        return type
    else:
        raise Exception("Illegal arguments exception!")


if __name__ == '__main__':
    c_occ_type = get_co_occurrence_type()
    PMI_dict = defaultdict(int_default_dict)
    inv_PMI = defaultdict(int_default_dict)
    word_count = pickle.load(open("word_counts_" + c_occ_type + ".save", "rb"))
    total_counts = get_total_count()
    create_PMI_from_counts()
    print("yay")
    pickle.dump(PMI_dict, open("pmi_dict_" + c_occ_type + ".save", "wb"))
    pickle.dump(inv_PMI, open("inv_pmi_dict_" + c_occ_type + ".save", "wb"))