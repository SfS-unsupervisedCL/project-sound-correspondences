# Reads the input from one or more CSV word lists generated by merge_lists.py
# and returns the set of IPA symbols across these files.

import sys


def get_symbols(dir):
    """
    Get the set of IPA symbols from the given CSV file.

    :param dir: directory of the file
    :type dir: str
    :return: set of IPA symbols
    :rtype: set(str)
    """

    symbols = set()

    with open(dir, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace(',', '').strip()
            symbols.update(process_line(line))

    return symbols


def process_line(line):
    """
    Convert a given string to a list of IPA symbols.

    >>> process_line('ɔˑzʲɪrə')
    ['ɔˑ', 'zʲ', 'ɪ', 'r','ə']
    >>> process_line('tʲɪt͡ʃʲeˑnʲijə')
    ['tʲ', 'ɪ', 't͡ʃʲ', 'eˑ', 'nʲ', 'i', 'j', 'ə']

    :param line: a given string
    :type line: str
    :return: list of IPA symbols
    :rtype: list[str]
    """

    symbols = []
    symbol_idx = 0

    while symbol_idx < len(line):
        s = line[symbol_idx]

        if s == '͡':
            symbols.append(symbols.pop() + line[symbol_idx:symbol_idx + 2])
            symbol_idx += 1
        elif s in 'ːˑʲ̯':
            symbols.append(symbols.pop() + s)
        else:
            symbols.append(s)

        symbol_idx += 1

    return symbols


if __name__ == "__main__":
    n_args = len(sys.argv)
    symbols = set()

    if n_args < 2:
        sys.stderr.write("Usage: %s INPUT\n" % sys.argv[0])
        sys.exit(1)

    for i in range(1, n_args):
        symbols.update(get_symbols(sys.argv[i]))

    print(symbols)
