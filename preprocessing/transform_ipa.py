import sys

phonetic_features = ['sound_type', 'manner', 'place', 'voice', 'secondary',
                     'length', 'vertical', 'horizontal', 'rounding',
                     'nasalization']


def list2dict(feat_list):
    """
    Transforms a list into a dictionary that maps the
    list elements to their indices within the list.
    """
    if feat_list is None:
        return None
    return dict([elem, index] for index, elem in enumerate(feat_list))


sound_type = ['', 'dot', 'word boundary', 'consonant', 'vowel']
# consonant articulation
manner = ['', 'plosive', 'tap', 'trill', 'affricate', 'fricative',
          'lateral fricative', 'lateral approximant', 'approximant',
          'nasal']
place = ['', 'glottal', 'pharyngeal', 'uvular', 'velar', 'palatal',
         'retroflex', 'alveolo-palatal', 'postalveolar', 'alveolar',
         'dental', 'labiodental', 'bilabial']
voice = ['', 'voiceless', 'voiced']
secondary = ['', 'pharyngealized', 'velarized', 'palatalized',
             'labialized', 'non-syllabic']
# consonant + vowel
length = ['', 'normal', 'half-long', 'long']
# vowel articulation
vertical = ['', 'open', 'near-open', 'open-mid', 'mid', 'close-mid',
            'near-close', 'close']
horizontal = ['', 'back', 'near-back', 'central', 'near-front',
              'front']
rounding = ['', 'unrounded', 'rounded']
nasalization = ['', 'nasalized']
lists = [None, sound_type, manner, place, voice, secondary,
         length, vertical, horizontal, rounding, nasalization]
dicts = [list2dict(lists[index]) for index in range(len(lists))]
phone_slots = [''] + phonetic_features
positions = {elem: index for index, elem in enumerate(phone_slots)}


def string2int(feature, value):
    """
    Transforms a string value from the IPA CSV file
    into the corresponding integer.

    Keyword arguments:
    feature -- the phonetic feature (i.e. the column name)
    value -- the string value for the feature
    """
    feature_index = positions[feature]
    return dicts[feature_index][value]


def int2string(feature, value):
    """
    Transforms an integer value back into a string value,
    corresponding to the information in the IPA CSV file.

    Keyword arguments:
    feature -- the phonetic feature (i.e. the column name)
    value -- the integer value for the feature, as assigned by this class
    """
    feature_index = positions[feature]
    return lists[feature_index][value]


def transform_ipa(in_file, out_file):
    """
    Transforms a CSV file containing string information on IPA symbols
    into a CSV containing the same information, but in integer format.
    The order of the columns has to be as follows:
    symbol, sound_type, manner, place, voice, secondary, length,
    vertical, horizontal, rounding, nasalization
    'sound_type' can take the following values:
    {vowel, consonant, dot, word boundary}
    The other values should follow the naming conventions from the IPA table.

    Keyword arguments:
    in_file -- the original file
    out_file -- the new file
    """
    with open(in_file, 'r', encoding='utf-8') as f_in:
        with open(out_file, 'w', encoding='utf-8') as f_out:
            for i, line in enumerate(f_in):
                if i == 0:
                    continue
                line = line.strip()
                fields = line.split(',')
                if len(fields) < 11:
                    sys.stderr.write('The following line is too short \
                                     (fewer than 11 fields). Skipping line.')
                    sys.stderr.write(line)
                    continue
                f_out.write(fields[0] + ",")
                for index in range(1, 11):
                    value = fields[index]
                    f_out.write(str(dicts[index][value]))
                    if index < 10:
                        f_out.write(",")
                f_out.write("\n")


if __name__ == '__main__':
    in_file = '../data/ipa.csv'
    out_file = '../data/ipa_numerical.csv'
    if len(sys.argv) > 2:
        in_file = sys.argv[1]
        out_file = sys.argv[2]
    transform_ipa(in_file, out_file)
