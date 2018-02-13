import preprocessing.transform_ipa as tipa

class Phone(object):
    """A class storing phonetic information about phone(me)s."""
    __slots__ = 'sound_type', 'manner', 'place', 'voice', 'secondary', 'vertical', 'horizontal', 'rounding', 'length', 'nasalization'

    def __init__(
            self, sound_type,
            manner, place, voice, secondary,
            length, vertical, horizontal,
            rounding, nasalization):
        self.sound_type = sound_type
        self.manner = manner
        self.place = place
        self.voice = voice
        self.secondary = secondary
        self.length = length
        self.vertical = vertical
        self.horizontal = horizontal
        self.rounding = rounding
        self.nasalization = nasalization

    def __repr__(self):
        return "{}({}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
            self.__class__.__name__,
            tipa.int2string('sound_type', self.sound_type),
            tipa.int2string('manner', self.manner),
            tipa.int2string('place', self.place),
            tipa.int2string('voice', self.voice),
            tipa.int2string('secondary', self.secondary),
            tipa.int2string('length', self.length),
            tipa.int2string('vertical', self.vertical),
            tipa.int2string('horizontal', self.horizontal),
            tipa.int2string('rounding', self.rounding),
            tipa.int2string('nasalization', self.nasalization))

    def distance(self, other):
        # TODO tweak the slots to allow for iteration?
        dist = 0
        if self.sound_type != other.sound_type:
            return 1
        # TODO different weights?
        # wrt scalar values (like vowel positions)
        if self.manner != other.manner:
            dist += 1
        if self.place != other.place:
            dist += 1
        if self.voice != other.voice:
            dist += 1
        if self.secondary != other.secondary:
            dist += 1
        if self.vertical != other.vertical:
            dist += 1
        if self.horizontal != other.horizontal:
            dist += 1
        if self.length != other.length:
            dist += 1
        if self.nasalization != other.nasalization:
            dist += 1
        dist /= (len(self.__slots__) - 1)
        return dist

    def equal(self, other):
        return self.distance(other) == 0

    def features(self):
        return [self.sound_type, self.manner,
                self.place, self.voice, self.secondary, self.vertical,
                self.horizontal, self.rounding, self.length, self.nasalization]
