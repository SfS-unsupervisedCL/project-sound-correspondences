import numpy as np


def generate_instances(levels, positions, sound_f, n_samples):
    """
    Create a numpy matrix of [n_samples, n_features] shape and 
    a list of column headers based on the information about contexts. 

    :param levels: For example, 'source' and 'target'.
    :type levels: list[str]
    :param positions: For example, 'itself', 'previous', etc.
    :type positions: list[str]
    :param sound_f: features of the sound. For example, 'manner', etc.
    :type sound_f: list[str]
    :param n_samples:
    :type n_samples: int
    :return: matrix to store data, list of feature types
    :rtype: list[str], np.matrix[np.int32] 
    """
    n_features = len(levels) * len(positions) * len(sound_f)
    matrix = np.zeros([n_samples, n_features], dtype=np.int32)
    headers = ["{}Lang_{}_{}".format(l, p, f) for l in levels for p in positions for f in sound_f]

    return matrix, headers

if __name__ == "__main__":
    m_example, f_example = generate_instances(
        ["source", "target"], ["itself", "previous"], ["manner", "voiced"], 10)
    print(m_example, "\n", f_example)