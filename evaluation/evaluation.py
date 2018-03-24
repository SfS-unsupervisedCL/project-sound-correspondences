import numpy as np
import pickle
from preprocessing import transform_ipa
from preprocessing import utils
from preprocessing.phone import Phone
from preprocessing.candidate_contexts import get_features
from preprocessing.features import header_list
from operator import itemgetter


def evaluation(lang_one, lang_two, cognates_file, ipa_file):
    """
    Generate words using the cognates from the second language and
    decision trees that describe sound transformation between two languages.
    Calculate the accuracy of predicted words using average Needleman-Wunsch.
    """
    ipa_dict = utils.read_ipa_dict(ipa_file)
    cognate_data, _ = utils.get_cognates(cognates_file, ipa_dict, 0.4, return_phones=True)
    cognate_pairs = [(word_one, word_two) for (_, word_one, word_two, _) in cognate_data]
    # Getting the names of levels from the cognates_file string
    levels = cognates_file.split("/")[-1].split("-")[:2]

    train_data_size = round(len(cognate_pairs) * 0.9)
    test_data = cognate_pairs[train_data_size:]
    total_nld = 0.0

    # Storing source and target words
    if lang_one == levels[0]:
        t_words, s_words = zip(*test_data)
    else:
        s_words, t_words = zip(*test_data)

    for pair_idx, _ in enumerate(test_data):
        src_word = s_words[pair_idx]
        target_word = t_words[pair_idx]

        w_length = len(src_word)
        predicted_word = _generate_template(w_len=w_length)
        header = header_list(levels)

        # store the labels of all phonetic features except sound type
        phonetic_features = transform_ipa.phonetic_features[1:]

        for sound_idx in range(w_length - 1):
            if lang_one in ["ukr", "swe"]:
                features_matrix = get_features(src_word, predicted_word)
            else:
                features_matrix = get_features(predicted_word, src_word)
            sound = []

            for feature_name in phonetic_features:
                removed_indices = [i for i, x in enumerate(header)
                                   if x.startswith(lang_one + "_itself") or
                                   x.startswith(lang_one + "_prevOrSelf")]
                label_col = header.index("{}_itself_{}".format(lang_one, feature_name))
                removed_indices.append(label_col)

                data = np.delete(features_matrix, removed_indices, 1)
                data = np.array(data[sound_idx, :]).reshape((1, -1))

                clf_file = "classifiers/{}_{}.pickle".format(lang_one, feature_name)
                with open(clf_file, 'rb') as handle:
                    clf = pickle.load(handle)

                predicted_feature = clf.predict(data)
                sound.append(predicted_feature[0])

            sound = [_detect_sound_type(sound)] + sound
            predicted_word[sound_idx + 1] = Phone(*sound)

        nld = utils.lev_distance(predicted_word, target_word, ipa_dict=ipa_dict)
        total_nld += nld

    n_words = len(test_data)
    average_nld = total_nld / n_words

    print("Results for '{}' based on '{}' language".format(lang_one, lang_two))
    print("{}: average NLD for {} test words".format(round(average_nld, 2), n_words))

def _generate_template(w_len):
    """
    Generate a template word. First phone is a word boundary. 
    All the other phones are dots. Later dots are replaced
    by predicted sounds.

    :param w_len: length of the word including word boundary
    :return: template word
    :rtype: list[Phone]
    """
    temp_word = [Phone(*[2, 0, 0, 0, 0, 0, 0, 0, 0, 0])] + \
                [Phone(*[1, 0, 0, 0, 0, 0, 0, 0, 0, 0]) for i in range(w_len - 1)]

    return temp_word


def _detect_sound_type(sound_features):
    """
    Detect a sound type (dot, consonant, vowel) based on its features.
    """
    consonantal_features = list(itemgetter(*[0, 1])(sound_features))
    vocalic_features = list(itemgetter(*[5, 6])(sound_features))

    if consonantal_features == vocalic_features == [0, 0]:
        return 1
    elif consonantal_features > vocalic_features:
        return 3
    else:
        return 4

if __name__ == "__main__":
    evaluation("deu", "swe", "../data/deu-swe-all.csv", "../data/ipa_numerical.csv")
    evaluation("swe", "deu", "../data/deu-swe-all.csv", "../data/ipa_numerical.csv")
    evaluation("rus", "ukr", "../data/rus-ukr-all.csv", "../data/ipa_numerical.csv")
    evaluation("ukr", "rus", "../data/rus-ukr-all.csv", "../data/ipa_numerical.csv")







