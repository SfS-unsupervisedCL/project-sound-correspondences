# Extracts the IPA columns from two NorthEuraLex CSV files, aligns the translations, and prints the new bilingual wordlist to a new CSV file. 

import sys

# concepts_y[x] contains the list of vocabulary items for concept no. x-1 in language y
concepts_1 = []
concepts_2 = []

def read_file(file, concepts):
	with open(file, 'r', encoding='utf-8') as f:
		header = next(f).split(',')
		concept_index = header.index('concept_id')
		ipa_index = header.index('raw_ipa')
		for line in f:
			cells = line.split(',')
			concept_id = int(cells[concept_index]) - 1
			ipa = cells[ipa_index]
			try:
				synonym_list = concepts[concept_id].append(ipa)
			except IndexError:
				concepts.append([ipa])

def print_file(lang1, lang2):
	n_concepts = len(concepts_1)
	assert(n_concepts == len(concepts_2))
	file = "../data/" + lang1 + '-' + lang2 + '-all.csv'
	with open(file, 'w', encoding='utf-8') as f:
		f.write('concept_id' + ',' + lang1 + ',' + lang2 + '\n')
		for concept in range(n_concepts):
			word_list_1 = concepts_1[concept]
			word_list_2 = concepts_2[concept]
			for word_1 in word_list_1:
				for word_2 in word_list_2:
					f.write(str(concept + 1) + ',' + word_1 + ',' + word_2 + '\n')

if __name__ == '__main__':
	if len(sys.argv) != 5:
		sys.stderr.write('Usage: %s LANG_NAME_1 WORDLIST_1 LANG_NAME_2 WORDLIST_2\n' % sys.argv[0])
		sys.exit(1)

	read_file(sys.argv[2], concepts_1)
	read_file(sys.argv[4], concepts_2)
	print_file(sys.argv[1], sys.argv[3])