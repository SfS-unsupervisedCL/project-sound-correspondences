class TransformIPA():

    __slots__ = 'lists', 'dicts', 'positions'

    def __init__(self):
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
        horizontal = ['', 'back', 'near-back', 'central', 'near-front',
                      'front']
        rounding = ['', 'unrounded', 'rounded']
        nasalization = ['', 'nasalized']
        self.lists = [None, sound_type, manner, place, voice, secondary,
                      length, vertical, horizontal, rounding, nasalization]
        self.dicts = [self.list2dict(self.lists[index]) for index in range(len(self.lists))]
        phone_slots = ['', 'sound_type', 'manner', 'place', 'voice',
                       'secondary', 'length', 'vertical', 'horizontal',
                       'rounding', 'nasalization']
        self.positions = {elem: index for index, elem in enumerate(phone_slots)}

    def list2dict(self, feat_list):
        if feat_list is None:
            return None
        return dict([elem, index] for index, elem in enumerate(feat_list))

    def string2int(self, feature, value):
        feature_index = self.positions[feature]
        return self.dicts[feature_index][value]

    def transform_ipa(self, in_file, out_file):
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
                        f_out.write(str(self.dicts[index][value]))
                        if index < 10:
                            f_out.write(",")
                    f_out.write("\n")


if __name__ == '__main__':
    tipa = TransformIPA()
    tipa.transform_ipa('ipa.csv', 'ipa_numerical.csv')
