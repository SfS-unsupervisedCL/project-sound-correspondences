import numpy as np
import copy
from preprocessing.phon_inventory import process_line
from phone import Phone

ipa_symbols = dict()


def read_ipa(ipa_file):
    ipa_symbols = dict()
    with open(ipa_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or len(line) == 0:
                continue
            # symbol,type,manner,place,voice,secondary,vertical,horizontal,rounding,length,nasalization
            # TODO make this dynamic instead?
            fields = line.split(',')
            assert len(fields) == 11
            symbol = fields[0]
            phone = Phone(sound_type=fields[1],
                          manner=fields[2], place=fields[3],
                          voice=fields[4], secondary=fields[5],
                          vertical=fields[6], horizontal=fields[7],
                          rounding=fields[8], length=fields[9],
                          nasalization=fields[10])
            ipa_symbols[symbol] = phone
    return ipa_symbols


def to_phone(symbol):
    if len(symbol) == 1:
        return copy.deepcopy(ipa_symbols[symbol])
    phone = copy.deepcopy(ipa_symbols[symbol[0]])
    print('symbol', symbol)
    if '͡' in symbol:
        # TODO diphthong
        phone.manner = 'affricate'
    if 'ʲ' in symbol:
        phone.secondary = 'palatalized'
    if 'ː' in symbol:
        phone.length = 'long'
    elif 'ˑ' in symbol:
        phone.length = 'half long'
    return phone


def lev_distance(w1, w2):
    """
    Calculate the modified levenshtein distance using phonological information about sounds.
    
    >>> lev_distance(['t', 'i'], ['t', 'a'])
    0.1
    >>> lev_distance(['t', 'i'], ['d', 'i'])
    0.3
    >>> lev_distance(['t', 'i'], ['a', 'i'])
    0.9
    
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

    return previous_row[-1]


def needleman_wunsch(word1, word2):
    """
    Implementation of the Needleman-Wunsch algorithm,
    which search for the optimal alignment of two sequences.
    
    >>> needleman_wunsch(['g', 'a', 't', 't', 'a', 'c', 'a'], ['g', 'c', 'a', 't', 'g', 'c', 'u'])
    [['g', '-', 'a', 't', 't', 'a', 'c', 'a']
     ['g', 'c', 'a', 't', '-', 'g', 'c', 'u']]
     
    >>> needleman_wunsch(['tʲ', 'ɪ', 't͡ʃʲ', 'eˑ'], ['tʲ', 'ɪ', 'eˑ'])
    [['tʲ', 'ɪ', '-', 'eˑ']
     ['tʲ', 'ɪ', 't͡ʃʲ', 'eˑ']]
    
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

    greed = np.zeros([len_w1 + 1, len_w2 + 1], dtype=int)
    # initialize the first column
    for i in range(len_w1 + 1):
        greed[i][0] = -i

    # initialize the first row
    for i in range(len_w2 + 1):
        greed[0][i] = -i

    # add missed numbers to the table
    for i, sound1 in enumerate(word1):
        for j, sound2 in enumerate(word2):
            top = greed[i][j + 1] - 1
            left = greed[i + 1][j] - 1

            if sound1 == sound2:
                top_left = greed[i][j] + (sound1 == sound2)
            else:
                top_left = greed[i][j] - 1

            greed[i + 1][j + 1] = max(top, left, top_left)

    # construct the best alignment
    align1 = []
    align2 = []
    trace = len_w1, len_w2

    while trace != (0, 0):
        i = trace[0]
        j = trace[1]

        top = greed[i - 1][j]
        left = greed[i][j - 1]
        top_left = greed[i - 1][j - 1]

        best = max(top, left, top_left)

        if top_left == best:
            align1 = [word1[i - 1]] + align1
            align2 = [word2[j - 1]] + align2
            trace = i - 1, j - 1
        elif left == best:
            align1 = ['-'] + align1
            align2 = [word2[j - 1]] + align2
            trace = i, j - 1
        else:
            align1 = [word1[i - 1]] + align1
            align2 = ['-'] + align2
            trace = i - 1, j

    return align1, align2


if __name__ == "__main__":
    ipa_symbols = read_ipa("preprocessing/ipa.csv")
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
    print(needleman_wunsch(process_line('GATTACA'), (process_line('GCATGCU'))))
    