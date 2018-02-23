import sys


def read_file(file):
    """
    Extracts the entries from a word list that is formatted like the ones from
    NorthEuraLex. It should be a CSV file with table headers, including
    'concept_id' and 'raw_ipa'. Each word should be on a separate row.

    Keyword arguments:
    file: the word list

    Returns:
    concepts: list(list(str))
              where concepts[x+1] contains the words for concept x
    """
    concepts = []
    with open(file, 'r', encoding='utf-8') as f:
        header = next(f).split(',')
        concept_index = header.index('concept_id')
        ipa_index = header.index('raw_ipa')
        for line in f:
            cells = line.split(',')
            concept_id = int(cells[concept_index]) - 1
            ipa = cells[ipa_index]
            try:
                concepts[concept_id].append(ipa)
            except IndexError:
                concepts.append([ipa])
    return concepts


def print_file(lang1, lang2, concepts_1, concepts_2, out_dir):
    """Prints the word lists, aligned by the concept IDs."""
    n_concepts = len(concepts_1)
    assert(n_concepts == len(concepts_2))
    file = out_dir + "/" + lang1 + '-' + lang2 + '-all.csv'
    with open(file, 'w', encoding='utf-8') as f:
        f.write('concept_id' + ',' + lang1 + ',' + lang2 + '\n')
        for concept in range(n_concepts):
            word_list_1 = concepts_1[concept]
            word_list_2 = concepts_2[concept]
            for word_1 in word_list_1:
                for word_2 in word_list_2:
                    f.write(str(concept + 1) + ',' + word_1
                                             + ',' + word_2 + '\n')


if __name__ == '__main__':
    if len(sys.argv) != 6:
        sys.stderr.write('Usage: %s LANG_NAME_1 WORDLIST_1 \
                                    LANG_NAME_2 WORDLIST_2 OUTPUT_DIR\n'
                         .format(sys.argv[0]))
        sys.exit(1)

    concepts1 = read_file(sys.argv[2])
    concepts2 = read_file(sys.argv[4])
    print_file(sys.argv[1], sys.argv[3], concepts1, concepts2, sys.argv[5])
