import numpy as np
import copy
from preprocessing.phon_inventory import process_line
from preprocessing.transform_ipa import TransformIPA
from phone import Phone

ipa_symbols = dict()
tipa = TransformIPA()


def read_ipa(ipa_file):
    ipa_symbols = dict()
    with open(ipa_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # symbol,type,manner,place,voice,secondary,vertical,horizontal,rounding,length,nasalization
            # TODO make this dynamic instead?
            fields = line.split(',')
            assert len(fields) == 11
            symbol = fields[0]
            phone = Phone(sound_type=int(fields[1]),
                          manner=int(fields[2]), place=int(fields[3]),
                          voice=int(fields[4]), secondary=int(fields[5]),
                          vertical=int(fields[6]), horizontal=int(fields[7]),
                          rounding=int(fields[8]), length=int(fields[9]),
                          nasalization=int(fields[10]))
            ipa_symbols[symbol] = phone
    return ipa_symbols


def to_phone(symbol):
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


def needleman_wunsch(word1, word2):
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
    :return: a pair of aligned sound representations of two words
    :rtype: tuple(str, str)
    """
    len_w1 = len(word1)
    len_w2 = len(word2)

    if len_w1 > len_w2:
        return needleman_wunsch(word2, word1)

    if len_w2 == 0:
        word2 = ['-' for i in range(len(word1))]
        return word1, word2

    grid = np.zeros([len_w1 + 1, len_w2 + 1], dtype=float)
    # initialize the first column
    for i in range(len_w1 + 1):
        grid[i][0] = -i

    # initialize the first row
    for i in range(len_w2 + 1):
        grid[0][i] = -i

    # add missed numbers to the table
    for i, sound1 in enumerate(word1):
        for j, sound2 in enumerate(word2):
            top = grid[i][j + 1] - 1
            left = grid[i + 1][j] - 1

            if sound1 == sound2:
                top_left = grid[i][j] + (sound1 == sound2)
            else:
                top_left = grid[i][j] - to_phone(sound1).distance(to_phone(sound2))

            grid[i + 1][j + 1] = max(top, left, top_left)

    print(grid)

    # construct the best alignment
    align1 = []
    align2 = []
    trace = len_w1, len_w2

    while trace != (0, 0):
        i = trace[0]
        j = trace[1]

        top = grid[i - 1][j]
        left = grid[i][j - 1]
        top_left = grid[i - 1][j - 1]

        best = max(top, left, top_left)

        if top_left == best:
            align1 = [to_phone(word1[i - 1])] + align1
            align2 = [to_phone(word2[j - 1])] + align2
            trace = i - 1, j - 1
        elif left == best:
            align1 = [to_phone('*')] + align1
            align2 = [to_phone(word2[j - 1])] + align2
            trace = i, j - 1
        else:
            align1 = [to_phone(word1[i - 1])] + align1
            align2 = [to_phone('*')] + align2
            trace = i - 1, j

    align1 = [to_phone('#')] + align1
    align2 = [to_phone('#')] + align2

    return align1, align2


if __name__ == "__main__":
    ipa_symbols = read_ipa("preprocessing/ipa_numerical.csv")
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
    print(needleman_wunsch(['a', 'p', 'a'], ['p', 'a']))

    result = needleman_wunsch(['a', 'p', 'a'], ['p', 'a'])
    for i in result:
        print(i)
