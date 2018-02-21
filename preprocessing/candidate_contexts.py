from . import transform_ipa as tipa
from .phone import Phone, attributes
import numpy as np


def get_features(source_w, target_w):
    n_features = len(attributes()) * 8  # 8 position features
    source_matrix = process_word(source_w, n_features)
    target_matrix = process_word(target_w, n_features)

    return np.concatenate((source_matrix, target_matrix), axis=1)


def process_word(word, n_features):
    w_matrix = np.zeros([len(word) - 1, n_features], dtype=np.int32)

    prev_sound = word[0]
    prev_non_dot = word[0]
    prev_cons = Phone()
    prev_vowel = Phone()

    for i in range(len(word) - 1):
        itself = word[i + 1]

        row = (itself.features() + prev_sound.features() + prev_non_dot.features()
               + prev_cons.features() + prev_vowel.features())

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

        row += self_non_dot.features() + self_cons.features() + self_vowel.features()

        w_matrix[i] = row
        prev_sound = itself

    return w_matrix


def check_type(sound, sound_type):
    return sound.sound_type == tipa.string2int('sound_type', sound_type)
