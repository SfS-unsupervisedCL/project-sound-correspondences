from . import transform_ipa as tipa
from .phone import Phone, attributes
import numpy as np

positions = ['itself', 'prev', 'prevNonDot', 'prevCons', 'prevVowel',
             'prevOrSelfNonDot', 'prevOrSelfCons', 'prevOrSelfVowel']


def get_features(source_w, target_w):
    """
    Creates a matrix containing the features for all sounds in the given words.

    Keyword arguments:
    source_w: The word in the source language.
              A list(Phone) as returned by utils.get_cognates.
    target_w: The word in the target language.
              A list(Phone) as returned by utils.get_cognates.

    Returns:
    A numpy matrix with 2 * n_phonetic_features * n_context_positions columns
    and len(source_w)-1 rows. The order of the columns matches that of the
    header created by features.generate_features.
    """
    n_features = len(attributes()) * len(positions)
    source_matrix = process_word(source_w, n_features)
    target_matrix = process_word(target_w, n_features)

    return np.concatenate((source_matrix, target_matrix), axis=1)


def process_word(word, n_features):
    """
    Creates a matrix containing the features for all sounds in the given word.

    Keyword arguments:
    word: The word--a list(Phone) as returned by utils.get_cognates

    Returns:
    w_matrix: A numpy matrix with n_phonetic_features * n_context_positions
              columns and len(word)-1 rows.
    """
    w_matrix = np.zeros([len(word) - 1, n_features], dtype=np.int32)

    prev_sound = word[0]
    prev_non_dot = word[0]
    prev_cons = Phone()
    prev_vowel = Phone()

    for i in range(len(word) - 1):
        itself = word[i + 1]

        row = (itself.features() + prev_sound.features()
               + prev_non_dot.features() + prev_cons.features()
               + prev_vowel.features())

        if not check_type(itself, "dot"):
            self_non_dot = itself
            prev_non_dot = itself
        else:
            self_non_dot = prev_non_dot

        if check_type(itself, "consonant"):
            self_cons = itself
            prev_cons = itself
        else:
            self_cons = prev_cons

        if check_type(itself, "vowel"):
            self_vowel = itself
            prev_vowel = itself
        else:
            self_vowel = prev_vowel

        row += (self_non_dot.features() + self_cons.features()
                + self_vowel.features())

        w_matrix[i] = row
        prev_sound = itself

    return w_matrix


def check_type(sound, sound_type):
    return sound.sound_type == tipa.string2int('sound_type', sound_type)
