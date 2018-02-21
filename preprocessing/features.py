from . import candidate_contexts
from . import phone
from . import utils
import numpy as np
import sys
import re


def generate_features(in_file, threshold=0.4, ipa_file="data/ipa_numerical.csv"):
    ipa_dict = utils.read_ipa_dict(ipa_file)
    cognates, _ = utils.get_cognates(in_file, ipa_dict, threshold, return_phones=True)

    all_features = []
    for (_, src_word, target_word, _) in cognates:
        features = candidate_contexts.get_features(src_word, target_word)
        all_features.append(features)
    all_features = np.vstack(all_features)
    print("extracted the features")

    # TODO clean this up
    out_file = re.sub('all', 'features', in_file)
    if '\\' in in_file:
        in_file = in_file.split('\\')[-1]
    elif '/' in in_file:
        in_file = in_file.split('/')[-1]
    levels = in_file.split('-')[:2]
    positions = ['itself', 'prev', 'prevNonDot', 'prevCons', 'prevVowel', 'prevOrSelfNonDot', 'prevOrSelfCons', 'prevOrSelfVowel']
    features = phone.attributes()
    header = ["{}_{}_{}".format(l, p, f) for l in levels for p in positions for f in features]
    header = ','.join(header)

    np.savetxt(out_file, all_features, fmt='%d', delimiter=',', header=header)
    print("saved the features in {}".format(out_file))

    
if __name__ == "__main__":
    # TODO threshold, ipa
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s BILINGUAL_WORD_LIST_FILE\n' % sys.argv[0])
        sys.exit(1)

    generate_features(sys.argv[1])