import operator
from _collections import defaultdict
import pickle
import sys

OTHER = "<other/>"
TARGET_WORDS = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']


def cosine(self, trg_word, pmi_u_att, context2word):
    DT = defaultdict()
    dt = Counter()

    for trg_word1 in TARGET_WORDS:
        trg_word = wtoi[trg_word1]
        for context in pmi_u_att[trg_word]:
            for other_word in context2word[context]:
                if other_word == context:
                    continue
                dt[other_word] += pmi_u_att[trg_word][context] * pmi_u_att[other_word][context]
        for word in dt:
            dt[word] /= (normalize(pmi_u_att[trg_word]) * (normalize(pmi_u_att[word])))
        DT[trg_word] = dt
    return DT



def get_similar_to_target():
    top20_dict = defaultdict(dict)
    for target in TARGET_WORDS:
    #    if target in wtoi.keys():
        print ("wtoi[" + target + "] is - " + str(wtoi[target]))
        target_dict = PMI_dict[wtoi[target]]
        attr_dict = dict(sorted(target_dict.items(), key=operator.itemgetter(1), reverse=True)[:21])
        top20_dict[target] = [itow[key] for key, _ in attr_dict.items() if key != OTHER]
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
    wtoi = pickle.load(open("word_to_index_" + c_occ_type + ".save", "rb"))
    itow = pickle.load(open("index_to_word_" + c_occ_type + ".save", "rb"))
    #print (wtoi)
    result = get_similar_to_target()
    write_result()
