from . import candidate_contexts
from . import transform_ipa as tipa
from . import utils
import numpy as np
import sys
import re


def generate_features(in_file, ipa_file, threshold=0.4, train_pct=1):
    """
    Generates a CSV file containing the (integer) features needed for creating
    a decision tree.

    Keyword arguments:
    in_file: a bilingual word list, as created by merge_lists
    ipa_file: the CSV file created by transform_ipa.transform_ipa
    threshold: the maximum NED for cognate pairs (default: 0.4)
    train_pct: percentage of the cognate pairs that are used for training
    """
    ipa_dict = utils.read_ipa_dict(ipa_file)
    cognates, _ = utils.get_cognates(in_file,
                                     ipa_dict,
                                     threshold,
                                     return_phones=True)
    total_data_pct = len(cognates)
    train_data_pct = round(total_data_pct * train_pct)
    print(train_data_pct)
    cognates = cognates[:train_data_pct]
    all_features = []
    for (_, src_word, target_word, _) in cognates:
        features = candidate_contexts.get_features(src_word, target_word)
        all_features.append(features)
    all_features = np.vstack(all_features)
    print("Extracted the features for {} out of {} words."
          .format(train_data_pct, total_data_pct))

    out_file = re.sub('all', 'features', in_file)
    levels = simple_file_name(in_file).split('-')[:2]
    header = ','.join(header_list(levels))
    np.savetxt(out_file, all_features,
               fmt='%d', delimiter=',', header=header, comments='')
    print("Saved the features in {}.".format(out_file))


def header_list(levels,
                positions=candidate_contexts.positions,
                phonetic_features=tipa.phonetic_features):
    """Generates a list of all feature combinations."""
    return ["{}_{}_{}".format(l, p, f)
            for l in levels
            for p in positions
            for f in phonetic_features]


def simple_file_name(file):
    """
    Given a path for a file, this strips away the directory information
    and returns the file name only.
    """
    if '\\' in file:
        return file.split('\\')[-1]
    if '/' in file:
        return file.split('/')[-1]
    return file


if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.stderr.write('Usage: %s BILINGUAL_WORD_LIST IPA_FILE ' +
                         'THRESHOLD TRAIN_DATA_PERCENTAGE\n'
                         .format(sys.argv[0]))
        sys.exit(1)

    generate_features(sys.argv[1], sys.argv[2],
                      float(sys.argv[3]), float(sys.argv[4]))
