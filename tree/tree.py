from sklearn import tree
from preprocessing import phone
import graphviz
import numpy as np
import re
import sys

phonetic_features = ['sound_type', 'manner', 'place', 'voice', 'secondary', 'length', 'vertical', 'horizontal', 'rounding', 'nasalization']
sound_type = ['', 'dot', 'word boundary', 'consonant', 'vowel']
# consonant articulation
manner = ['', 'plosive', 'tap', 'trill', 'affricate', 'fricative',
          'lateral fricative', 'lateral approximant', 'approximant',
          'nasal']
place = ['', 'glottal', 'pharyngeal', 'uvular', 'velar', 'palatal',
         'retroflex', 'alveolo-palatal', 'postalveolar', 'alveolar',
         'dental', 'labiodental', 'bilabial']
voice = ['', 'voiceless', 'voiced']
secondary = ['', 'pharyngealized', 'velarized', 'palatalized',
             'labialized', 'non-syllabic']
# consonant + vowel
length = ['', 'normal', 'half-long', 'long']
# vowel articulation
vertical = ['', 'open', 'near-open', 'open-mid', 'mid', 'close-mid',
            'near-close', 'close']
horizontal = ['', 'back', 'near-back', 'central', 'near-front',
              'front']
rounding = ['', 'unrounded', 'rounded']
nasalization = ['', 'nasalized']
all_features_lists = [sound_type, manner, place, voice, secondary, length, vertical, horizontal, rounding, nasalization]
features_dict = dict(zip(phonetic_features[1:], all_features_lists[1:]))
languages = ["deu", "swe"]


def actual_class_names(labels, class_names_all):
    """
	Returns a list containing the names of the classes
	that actually appear in the data.
	The resulting list can be used as the class_names argument of
	sklearn.tree.export_graphviz.

	Keyword arguments:
	labels -- the column that the tree should predict
	class_names_all -- the list of class names, as given in transform_ipa
	"""
    unique = np.unique(labels).tolist()
    return [class_names_all[i] for i in unique]


def build_tree(in_file, out_dir, feature, types):
    # predict deu_itself_manner
    # feature = "deu_itself_manner"
    with open(in_file, 'r', encoding='utf-8') as f:
        header = f.readlines()[0].split(',')
    n_cols = len(header)
    label_col = header.index(feature)
    lang = feature.split("_")[0]
    removed_indices = [i for i, x in enumerate(header) if x.startswith(lang + "_prevOrSelf")]
    header.pop(label_col)

    data_cols = list(range(n_cols))
    data_cols.remove(label_col)
    # Remove indices of columns that contain data about "previousOrSelfSound" of source language
    data_cols = [i for j, i in enumerate(data_cols) if j not in removed_indices]

    labels = np.loadtxt(open(in_file, 'r'), delimiter=",", dtype=np.int32, skiprows=1, usecols=label_col)
    data = np.loadtxt(open(in_file, 'r'), delimiter=",", dtype=np.int32, skiprows=1, usecols=data_cols)

    # TODO import this list
    class_names = actual_class_names(labels, types)

    clf = tree.DecisionTreeClassifier(criterion='entropy')
    clf = clf.fit(data, labels)

    dot_data = tree.export_graphviz(clf, out_file=None,
                                    feature_names=header,
                                    class_names=class_names,
                                    filled=True,  # colour + hue by class + certainty
                                    rounded=True,  # purely cosmetic
                                    special_characters=True  # less-than-or-equals sign
                                    )

    graph = graphviz.Source(dot_data)
    outfile = out_dir + '/' + re.sub('itself_', '', feature)
    graph.render(outfile)

def build_trees(in_file, out_dir):
    features = ["{}_itself_{}".format(language, key) for language in languages for key in features_dict]

    for feature in features:
        types = features_dict[feature.split("_")[-1]]
        build_tree(in_file, out_dir, feature, types)

if __name__ == "__main__":
    # if len(sys.argv) < 3:
    #     sys.stderr.write('Usage: %s FEATURES OUTPUT_DIR\n' % sys.argv[0])
    #     sys.exit(1)
    #
    # build_trees(sys.argv[1], sys.argv[2])
    build_trees("../data/deu-swe-features.csv", "../output/")

