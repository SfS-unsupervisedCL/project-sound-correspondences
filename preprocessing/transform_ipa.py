def init():
    sound_type = ['dot', 'word boundary', 'consonant', 'vowel']
    # consonant articulation
    manner = ['', 'plosive', 'tap', 'trill', 'affricate', 'fricative',
              'lateral fricative', 'lateral approximant', 'approximant',
              'nasal']
    place = ['', 'glottal', 'pharyngeal', 'uvular', 'velar', 'palatal',
             'retroflex', 'alveolo-palatal', 'postalveolar', 'alveolar',
             'dental', 'labiodental', 'bilabial']
    voice = ['', 'voiceless', 'voiced']
    secondary = ['', 'pharyngealized', 'velarized', 'palatalized',
                 'labialized']
    # consonant + vowel
    length = ['', 'normal', 'half-long', 'long']
    # vowel articulation
    vertical = ['', 'open', 'near-open', 'open-mid', 'mid', 'close-mid',
                'near-close', 'close']
    horizontal = ['', 'back', 'near-back', 'central', 'near-front', 'front']
    rounding = ['', 'unrounded', 'rounded']
    nasalization = ['', 'nasalized']
    lists = [None, sound_type, manner, place, voice, secondary,
             length, vertical, horizontal, rounding, nasalization]
    dicts = [list2dict(lists[index]) for index in range(len(lists))]
    return lists, dicts


def list2dict(feat_list):
    if feat_list is None:
        return None
    return dict([elem, index] for index, elem in enumerate(feat_list))


def transform_ipa(in_file, out_file, lists, dicts):
    with open(in_file, 'r', encoding='utf-8') as f_in:
        with open(out_file, 'w', encoding='utf-8') as f_out:
            for i, line in enumerate(f_in):
                if i == 0:
                    continue
                line = line.strip()
                fields = line.split(',')
                assert len(fields) == 11
                f_out.write(fields[0] + ",")
                for index in range(1, 11):
                    value = fields[index]
                    f_out.write(str(dicts[index][value]))
                    if index < 10:
                        f_out.write(",")
                f_out.write("\n")


if __name__ == '__main__':
    lists, dicts = init()
    transform_ipa('ipa.csv', 'ipa_numerical.csv', lists, dicts)
