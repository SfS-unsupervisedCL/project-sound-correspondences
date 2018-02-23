from sklearn import tree
from preprocessing import transform_ipa as tipa
from preprocessing.features import simple_file_name
import graphviz
import numpy as np
import re
import sys

all_features_lists = [tipa.sound_type, tipa.manner, tipa.place, tipa.voice,
                      tipa.secondary, tipa.length, tipa.vertical,
                      tipa.horizontal, tipa.rounding, tipa.nasalization]
features_dict = dict(zip(tipa.phonetic_features[1:], all_features_lists[1:]))


def build_tree(in_file, out_dir, feature, types):
    feature_name = re.sub('itself_', '', feature)
    print("Building the tree for {}.".format(feature_name))

    with open(in_file, 'r', encoding='utf-8') as f:
        header = f.readlines()[0].split(',')

    if '# ' in header[0]:
        header[0] = header[0][2:]

    # exclude certain information from the training data:
    # - the column that we want to predict (label_col)
    # - columns about features that are too similar to label_col
    #   (prevOrSelfNonDot, prevOrSelfConsonant, prevOrSelfVowel
    #    for the language level we are currently considering)
    lang = feature.split("_")[0]
    removed_indices = [i for i, x in enumerate(header)
                       if x.startswith(lang + "_prevOrSelf")]
    label_col = header.index(feature)
    removed_indices.append(label_col)

    data_cols = list(range(len(header)))
    data_cols = [x for i, x in enumerate(data_cols)
                 if i not in removed_indices]
    header = [header[i] for i in range(len(header))
              if i not in removed_indices]

    labels = np.loadtxt(in_file,
                        delimiter=",",
                        dtype=np.int32,
                        skiprows=1,  # skip the header row
                        usecols=label_col)
    data = np.loadtxt(in_file,
                      delimiter=",",
                      dtype=np.int32,
                      skiprows=1,
                      usecols=data_cols)

    # get the names of the classes  that actually appear in the data
    unique = np.unique(labels).tolist()
    class_names = [types[i] for i in unique]

    clf = tree.DecisionTreeClassifier(
        criterion='entropy',
        min_impurity_decrease=0.01,
        min_samples_leaf=0.01)
    clf = clf.fit(data, labels)

    dot_data = tree.export_graphviz(clf,
                                    out_file=None,
                                    feature_names=header,
                                    class_names=class_names,
                                    # colour (class), saturation (certainty)
                                    filled=True,
                                    rounded=True,
                                    special_characters=True)
    graph = graphviz.Source(dot_data)
    outfile = out_dir + '/' + feature_name
    graph.render(outfile)


def build_trees(in_file, out_dir):
    languages = simple_file_name(in_file).split("-")[:2]
    features = ["{}_itself_{}".format(language, key)
                for language in languages
                for key in features_dict]
    for feature in features:
        # phon_feat = feature.split("_")[-1]
        # if 'sound_type' in feature:
        #     phon_feat = 'sound_type'
        # types = features_dict[phon_feat]
        types = features_dict[feature.split("_")[-1]]
        build_tree(in_file, out_dir, feature, types)
    print("Done.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write('Usage: %s FEATURES OUTPUT_DIR\n' % sys.argv[0])
        sys.exit(1)
    build_trees(sys.argv[1], sys.argv[2])
