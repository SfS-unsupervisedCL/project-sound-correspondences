from sklearn import tree
import graphviz
import numpy as np
import re
import sys

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


def build_tree(in_file, out_dir):
	# predict deu_itself_manner
	feature = "deu_itself_manner"
	with open(in_file, 'r', encoding='utf-8') as f:
		header = f.readlines()[0].split(',')
	n_cols = len(header)
	label_col = header.index("deu_itself_manner")
	header.pop(label_col)

	data_cols = list(range(n_cols))
	data_cols.remove(label_col)
	labels = np.loadtxt(open(in_file, 'r'), delimiter=",", dtype=np.int32, skiprows=1, usecols=label_col)
	data = np.loadtxt(open(in_file, 'r'), delimiter=",", dtype=np.int32, skiprows=1, usecols=data_cols)

	# TODO import this list
	class_names = actual_class_names(labels, ['', 'plosive', 'tap', 'trill', 'affricate', 'fricative',
                 'lateral fricative', 'lateral approximant', 'approximant',
                 'nasal'])

	clf = tree.DecisionTreeClassifier(criterion='entropy')
	clf = clf.fit(data, labels)

	dot_data = tree.export_graphviz(clf, out_file=None, 
		feature_names=header, 
		class_names=class_names,
		filled=True, # colour + hue by class + certainty
		rounded=True, # purely cosmetic
		special_characters=True # less-than-or-equals sign
		)

	graph = graphviz.Source(dot_data)
	outfile = out_dir + '/' + re.sub('itself_', '', feature)
	graph.render(outfile) 


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write('Usage: %s FEATURES OUTPUT_DIR\n' % sys.argv[0])
        sys.exit(1)

    build_tree(sys.argv[1], sys.argv[2])
