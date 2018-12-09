import operator
from _collections import defaultdict
import pickle
import sys

OTHER = "<other/>"
TARGET_WORDS = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']


def get_similar_to_target():
    top20_dict = defaultdict(dict)
    for target in TARGET_WORDS:
        target_dict = PMI_dict[target]
        attr_dict = dict(sorted(target_dict.items(), key=operator.itemgetter(1), reverse=True)[:21])
        top20_dict[target] = [key for key, _ in attr_dict.items() if key != OTHER]
    return top20_dict


def int_default_dict():
    return defaultdict(int)


def write_result():
    with open('Top 20 most similar - ' + c_occ_type, 'w') as file:
        for target, sim_words in result.items():
            file.write(target + '\n')
            file.write('\t'.join(sim_words) + '\n\n')


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
    PMI_dict = pickle.load(open("pmi_dict_" + c_occ_type + ".save", "rb"))
    inv_PMI = pickle.load(open("inv_pmi_dict_" + c_occ_type + ".save", "rb"))
    result = get_similar_to_target()
    write_result()