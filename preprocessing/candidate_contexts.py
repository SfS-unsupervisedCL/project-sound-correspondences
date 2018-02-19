from phone import Phone
import transform_ipa as tipa
import phon_inventory
import utils


def prev_non_dot(word, index, include_self=False):
    """
    Returns the previous non-dot symbol. If include_self is True and the
    symbol itself is a non-dot symbol, this method returns the symbol itself.

    Keyword arguments:
    word -- a list of Phone objects starting with a "word boundary" phone,
            like the lists returned by utils.needleman_wunsch
    index -- a position within the word (should be > 0, < len(word))
    include_self -- whether the symbol itself should be included
                    in the search (default: False)
    """
    i = index if include_self else index - 1
    while i > -1:
        if word[i].sound_type != tipa.string2int('sound_type', 'dot'):
            return word[i]
        i -= 1
    # this shouldn't happen since the words should start with a word boundary
    return Phone()  # all features are 0


def prev_consonant(word, index, include_self=False):
    """
    Returns the previous consonant. If include_self is True and the
    symbol itself is a consonant, this method returns the symbol itself.

    Keyword arguments:
    word -- a list of Phone objects starting with a "word boundary" phone,
            like the lists returned by utils.needleman_wunsch
    index -- a position within the word (should be > 0, < len(word))
    include_self -- whether the symbol itself should be included
                    in the search (default: False)
    """
    return _prev_sound_type('consonant', word, index, include_self)


def prev_vowel(word, index, include_self=False):
    """
    Returns the previous vowel. If include_self is True and the
    symbol itself is a vowel, this method returns the symbol itself.

    Keyword arguments:
    word -- a list of Phone objects starting with a "word boundary" phone,
            like the lists returned by utils.needleman_wunsch
    index -- a position within the word (should be > 0, < len(word))
    include_self -- whether the symbol itself should be included
                    in the search (default: False)
    """
    return _prev_sound_type('vowel', word, index, include_self)


def _prev_sound_type(sound_type, word, index, include_self):
    i = index if include_self else index - 1
    while i > -1:
        if word[i].sound_type == tipa.string2int('sound_type', sound_type):
            return word[i]
        i -= 1
    return Phone()  # all features are 0


if __name__ == "__main__":
    word = '#kæt'
    print(word)
    word = phon_inventory.process_line(word)
    ipa = utils.read_ipa('../data/ipa_numerical.csv')
    word = [utils.to_phone(symbol, ipa) for symbol in word]
    print(word)
    print('positional features for \'t\'')
    print('itself', word[3])
    print('previous position', word[2])
    print('previous non-dot symbol', prev_non_dot(word, 3))
    print('previous consonant', prev_consonant(word, 3))
    print('previous vowel', prev_vowel(word, 3))
    print('previous or self non-dot symbol', prev_non_dot(word, 3, True))
    print('previous or self consonant', prev_consonant(word, 3, True))
    print('previous or self vowel', prev_vowel(word, 3, True))
