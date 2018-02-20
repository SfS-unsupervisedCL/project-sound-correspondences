from sklearn import tree
import graphviz
import numpy as np


def build_tree(in_file):
	# predict deu_itself_manner
	with open(in_file, 'r', encoding='utf-8') as f:
		header = f.readlines()[0].split(',')
	n_cols = len(header)
	label_col = header.index("deu_itself_manner")
	header.pop(label_col)

	data_cols = list(range(n_cols))
	data_cols.remove(label_col)
	# print("label", label_col)
	# print("data", data_cols)
	labels = np.loadtxt(open(in_file, 'r'), delimiter=",", skiprows=1, usecols=label_col)
	data = np.loadtxt(open(in_file, 'r', encoding='utf-8'), delimiter=",", skiprows=1, usecols=data_cols)

	# print(data.shape)
	# print(labels.shape)
	# print(data[:10])
	# print(labels[:1])

	clf = tree.DecisionTreeClassifier(criterion='entropy')
	clf = clf.fit(data, labels)

	dot_data = tree.export_graphviz(clf, out_file=None, 
		feature_names=header, 
		# TODO import this
		class_names=['', 'plosive', 'tap', 'trill', 'affricate', 'fricative',
          'lateral fricative', 'lateral approximant', 'approximant',
          'nasal'],
		filled=True, # colour + hue by class + certainty
		rounded=True, # purely cosmetic
		special_characters=True # less-than-or-equals sign
		)
	graph = graphviz.Source(dot_data) 
	graph.render("deu_manner") 


if __name__ == "__main__":
	in_file = "../data/deu-swe-features.csv"
	build_tree(in_file)