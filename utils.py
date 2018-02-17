import numpy as np
import copy
import re
import pandas
from preprocessing.phon_inventory import process_line
import preprocessing.transform_ipa as tipa
from phone import Phone

ipa_symbols = dict()


def read_ipa(ipa_file):
    """
    Extracts the information contained in the CSV file created by
    preprocessing.transform_ipa.transform_ipa.
    """
    ipa_symbols = dict()
    with open(ipa_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            fields = line.split(',')
            assert len(fields) == 11
            symbol = fields[0]
            phone = Phone(sound_type=int(fields[1]),
                          manner=int(fields[2]), place=int(fields[3]),
                          voice=int(fields[4]), secondary=int(fields[5]),
                          length=int(fields[6]), vertical=int(fields[7]),
                          horizontal=int(fields[8]), rounding=int(fields[9]),
                          nasalization=int(fields[10]))
            ipa_symbols[symbol] = phone
    return ipa_symbols


def to_phone(symbol):
    """Transforms an IPA symbol into an instance of phone.Phone."""
    if len(symbol) == 1:
        return copy.deepcopy(ipa_symbols[symbol])
    phone = copy.deepcopy(ipa_symbols[symbol[0]])
    if '͡' in symbol:
        phone.manner = tipa.string2int('manner', 'affricate')
    if 'ʲ' in symbol:
        phone.secondary = tipa.string2int('secondary', 'palatalized')
    if 'ː' in symbol:
        phone.length = tipa.string2int('length', 'long')
    elif 'ˑ' in symbol:
        phone.length = tipa.string2int('length', 'half-long')
    elif '̯' in symbol:
        phone.length = tipa.string2int('secondary', 'non-syllabic')
    return phone


def lev_distance(w1, w2):
    """
    Calculate the normalized modified levenshtein distance using phonological information about sounds.
    
    >>> lev_distance(['t', 'i'], ['d', 'i'])
    0.05555555555555555
    >>> lev_distance(['t', 'i'], ['a', 'i'])
    0.5
    >>> lev_distance(['a', 't'], ['t', 'a'])
    1.0
    
    :param w1: first word
    :type: [str]
    :param w2: second word
    :type: [str]
    :return: levenshtein distance
    :rtype: float
    """
    if len(w1) < len(w2):
        return lev_distance(w2, w1)

    if len(w2) == 0:
        return float(len(w1))

    previous_row = range(len(w2) + 1)

    for i, symbol1 in enumerate(w1):
        current_row = [i + 1]

        for j, symbol2 in enumerate(w2):
            top = previous_row[j + 1] + 1
            left = current_row[j] + 1
            top_left = previous_row[j] + to_phone(symbol1).distance(to_phone(symbol2))
            current_row.append(min(top, left, top_left))
        previous_row = current_row

    return previous_row[-1] / len(w1)


def needleman_wunsch(word1, word2, print_matrix=False):
    """
    Implementation of the Needleman-Wunsch algorithm,
    which search for the optimal alignment of two sequences.
     
    >>> needleman_wunsch(['a', 'p', 'a'], ['p', 'a'])
    [[Phone(1 0 0 0 0 0 0 0 0 0), Phone(0 0 0 0 0 0 0 0 0 0), Phone(2 1 12 1 0 1 0 0 0 0), Phone(3 0 0 0 0 1 1 5 1 0)],
     [Phone(1 0 0 0 0 0 0 0 0 0), Phone(3 0 0 0 0 1 1 5 1 0), Phone(2 1 12 1 0 1 0 0 0 0), Phone(3 0 0 0 0 1 1 5 1 0)]]
     
    The transformed numerical output above represents the following alignment:
    [['#', 'a', 'p', 'a'],
     ['#', '*', 'p', 'a']]
    
    :param word1: sound representation of the first word
    :type word1: list[str]
    :param word2: sound representation of the second word
    :type word2: list[str]
    :param print_matrix:
    :type print_matrix: bool
    :return: a pair of aligned sound representations of two words
    :rtype: tuple(str, str)
    """
    len_w1 = len(word1)
    len_w2 = len(word2)

    # transition scores:
    # gap (insertion/deletion): -1
    # (mis)match: if phonetic distance > 0.5 then -1 (mismatch)
    gap_score = -1

    if len_w1 > len_w2:
        align2, align1 = needleman_wunsch(word2, word1, print_matrix)
        return align1, align2

    if len_w2 == 0:
        word2 = ['-' for i in range(len(word1))]
        return word1, word2

    score_grid = np.zeros([len_w1 + 1, len_w2 + 1], dtype=float)
    trace_grid = [[] for i in range(len_w1 + 1)]

    # initialize the first column
    trace_grid[0] = ['x']
    for i in range(len_w1 + 1):
        score_grid[i][0] = i * gap_score
        if i > 0:
            trace_grid[i].append('top')
            for j in range(len_w2):
                trace_grid[i].append('')

    # initialize the first row
    for i in range(len_w2 + 1):
        score_grid[0][i] = i * gap_score
    trace_grid[0] += ['left' for i in range(len_w2)]

    # fill in the table
    for i, sound1 in enumerate(word1):
        for j, sound2 in enumerate(word2):
            top = score_grid[i][j + 1] + gap_score
            left = score_grid[i + 1][j] + gap_score

            phone_dist = to_phone(sound1).distance(to_phone(sound2))
            if phone_dist < 0.5:
                top_left = score_grid[i][j] + 2 - phone_dist
            else:
                top_left = score_grid[i][j] - 1

            scores = {'top': top, 'left': left, 'top_left': top_left}
            max_score = max(scores.values())
            score_grid[i + 1][j + 1] = max_score
            delta = 0.0000001
            traces = [trace for trace, score in scores.items() if abs(max_score - score) < delta]
            # for now, let's only generate one alignment, even if there are several ones possible
            # we prioritize (mis)matches over insertions/deletions
            trace = traces[0]
            if len(traces) > 1:
                if abs(max_score - top_left) < delta:
                    trace = 'top_left'

            trace_grid[i + 1][j + 1] = trace

    # construct the best alignment
    align1 = []
    align2 = []
    i = len_w1
    j = len_w2

    while i > 0 or j > 0:
        trace = trace_grid[i][j]
        if trace == 'top_left':
            align1 = [word1[i - 1]] + align1
            align2 = [word2[j - 1]] + align2
            i -= 1
            j -= 1
        elif trace == 'left':
            align1 = ['*'] + align1
            align2 = [word2[j - 1]] + align2
            j -= 1
        else: # trace == 'top'
            align1 = [word1[i - 1]] + align1
            align2 = ['*'] + align2
            i -= 1

    align1 = ['#'] + align1
    align2 = ['#'] + align2

    if print_matrix:
        column_labels = ["0"] + word2
        row_labels = ["0"] + word1
        df = pandas.DataFrame(score_grid, columns=column_labels, index=row_labels)
        print(df)
        print()
        df = pandas.DataFrame(trace_grid, columns=column_labels, index=row_labels)
        print(df)

    return align1, align2


def get_cognates(file, threshold=0.5):
    """
    Determine possible cognates using Normalized Levenshtein Distance.
    Align pairs before applying NLD.
    
    :param file: directory of the file
    :type file: str
    :param threshold: argument for NLD
    :type threshold: float
    :return: 
    """
    with open(file, 'r', encoding='utf-8') as f:
        content = f.readlines()[1:]

    cognates = []
    not_cognates = []

    for line in content:
        line = re.sub(u'[\uFEFF\s|ˈˌ-]', '', line)

        concept_id, word1, word2 = line.split(',')
        concept_id = int(concept_id)
        word1 = process_line(word1)
        word2 = process_line(word2)

        word1, word2 = needleman_wunsch(word1, word2)
        ld = lev_distance(word1, word2)
        # word1 = ''.join(word1[1:])
        # word2 = ''.join(word2[1:])
        entry = (concept_id,word1,word2,round(ld, 2))
        if ld < threshold:
            cognates.append(entry)
        else:
            not_cognates.append(entry)

    return cognates, not_cognates


def print_cognates(file, threshold=0.5):
    cognates, non_cognates = get_cognates(file, threshold)
    file_cog = re.sub('all', 'cognates', file)
    file_non_cog = re.sub('all', 'non-cognates', file)

    with open(file, 'r', encoding='utf-8') as f:
        header = f.readlines()[0]
    header = header[:-1] + ',distance\n'

    for file, entries in zip([file_cog, file_non_cog], [cognates, non_cognates]):
        with open(file, 'w', encoding='utf-8') as f:
            f.write(header)
            for entry in entries:
                f.write(str(entry)[1:-1] + '\n')

if __name__ == "__main__":
    ipa_symbols = read_ipa("data/ipa_numerical.csv")
    word = 'tʲɪt͡ʃʲeˑnʲijə'
    word_symbols = process_line(word)
    # ['tʲ', 'ɪ', 't͡ʃʲ', 'eˑ', 'nʲ', 'i', 'j', 'ə']
    word_phones = []
    for symbol in word_symbols:
        word_phones.append(to_phone(symbol))
    print(word)
    print(word_symbols)
    print(word_phones)
    print(word_symbols[0], word_symbols[1], word_phones[0].distance(word_phones[1]))
    print(word_symbols[0], word_symbols[4], word_phones[0].distance(word_phones[4]))
    print(word_symbols[1], word_symbols[3], word_phones[1].distance(word_phones[3]))
    print(word_symbols[1], word_symbols[7], word_phones[1].distance(word_phones[7]))
    print('t', to_phone('t'))
    print('t', 'd', to_phone('t').distance(to_phone('d')))
    print('t', 't', to_phone('t').distance(to_phone('t')))
    print('t', 'm', to_phone('t').distance(to_phone('m')))
    # print(needleman_wunsch(['a', 'p', 'a'], ['p', 'a']))

    result = needleman_wunsch(['a', 'p', 'a'], ['p', 'a'])
    for i in result:
        print(i)

    result = needleman_wunsch(['h', 'ɛ', 'ɐ̯', 'b', 's', 't'], ['h', 'ø', 'sː', 't'], print_matrix=True)
    for i in result:
        print(i)

    print_cognates('data/deu-swe-all.csv', 0.4)
    print_cognates('data/rus-ukr-all.csv', 0.4)