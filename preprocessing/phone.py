from . import transform_ipa as tipa


class Phone(object):
    """A class storing phonetic information about phone(me)s."""
    __slots__ = tipa.phonetic_features

    def __init__(
            self, sound_type=0,
            manner=0, place=0, voice=0, secondary=0,
            length=0, vertical=0, horizontal=0,
            rounding=0, nasalization=0):
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
        """Human-readable string representation."""
        attributes = []
        for slot in self.__slots__:
            slot_val = getattr(self, slot)
            attributes.append(tipa.int2string(slot, slot_val))
        return "{}({}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
                self.__class__.__name__, *attributes)

    def attributes(self):
        """Returns the canonical order of the phonetic features."""
        return self.__slots__

    def features(self):
        """Returns this phone's attributes as a list of integers."""
        return [getattr(self, slot) for slot in self.__slots__]

    def distance(self, other):
        """
        Returns the phonetic distance to another phone.

        Keyword arguments:
        other -- another Phone object

        Returns:
        A float in the range [0, 1] where 0 means the phones are identical
        and 1 means that they are maximally different.
        """
        if self.sound_type != other.sound_type:
            return 1
        if self == other:
            return 0

        dist = 0
        max_dist = 1
        sound_type = tipa.int2string('sound_type', self.sound_type)

        if sound_type == 'consonant':
            max_dist = 5
            if self.manner != other.manner:
                manner_self = tipa.int2string('manner', self.manner)
                manner_other = tipa.int2string('manner', other.manner)
                if manner_self == 'affricate':
                    if manner_other == 'plosive' or manner_other == 'fricative':
                        dist += 0.5
                elif manner_other == 'affricate':
                    if manner_self == 'plosive' or manner_self == 'fricative':
                        dist += 0.5
                else:
                    dist += 1
            if self.place != other.place:
                if abs(self.place - other.place) < 3:
                    dist += 0.5
                else:
                    dist += 1
            if self.voice != other.voice:
                dist += 1

        if sound_type == 'consonant' or sound_type == 'vowel':
            if self.secondary != other.secondary:
                dist += 1
            if self.length != other.length:
                dist += 1

        if sound_type == 'vowel':
            max_dist = 6
            if self.vertical != other.vertical:
                if abs(self.vertical - other.vertical) < 3:
                    dist += 0.5
                else:
                    dist += 1
            if self.horizontal != other.horizontal:
                if abs(self.horizontal - other.horizontal) < 3:
                    dist += 0.5
                else:
                    dist += 1
            if self.nasalization != other.nasalization:
                dist += 1
            if self.rounding != other.rounding:
                dist += 1

        dist /= max_dist
        return dist

    def equals(self, other):
        return self.distance(other) == 0


def attributes():
    """Returns the canonical order of the phonetic features."""
    return Phone().attributes()

if __name__ == "__main__":
    p = Phone(*[1, 9, 1, 1, 2, 2, 2, 1, 1, 1])
    print(p)
    print(p.attributes())
    print(p.features())
