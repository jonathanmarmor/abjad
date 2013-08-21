# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.Segment import Segment


class NamedPitchSegment(Segment):
    '''Abjad model of a named chromatic pitch segment:

    ::

        >>> pitchtools.NamedPitchSegment(
        ...     ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"])
        NamedPitchSegment("bf bqf fs' g' bqf g'")

    Named chromtic pitch segments are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### CONSTRUCTOR ###

    def __new__(self, *args):
        from abjad.tools import pitchtools
        if len(args) == 1 and isinstance(args[0], str):
                pitches = [pitchtools.NamedPitch(x) 
                    for x in args[0].split()]
        else:
            pitches = [pitchtools.NamedPitch(x) for x in args[0]]
        return tuple.__new__(self, pitches)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s("%s")' % (self._class_name, self._repr_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_string(self):
        return ', '.join([str(x) for x in self])

    @property
    def _repr_string(self):
        return ' '.join([str(x) for x in self])

    ### PUBLIC PROPERTIES ###

    @property
    def chromatic_pitch_numbers(self):
        return [abs(pitch.numbered_chromatic_pitch) for pitch in self]

    @property
    def harmonic_chromatic_interval_class_segment(self):
        return [x.interval_class 
            for x in self.harmonic_chromatic_interval_segment]

    @property
    def harmonic_chromatic_interval_segment(self):
        from abjad.tools import pitchtools
        result = list(
            mathtools.difference_series(self.chromatic_pitch_numbers))
        result = [-x for x in result]
        return pitchtools.HarmonicChromaticIntervalSegment(result)

    @property
    def harmonic_diatonic_interval_class_segment(self):
        return [x.interval_class 
            for x in self.harmonic_diatonic_interval_segment]

    @property
    def harmonic_diatonic_interval_segment(self):
        from abjad.tools import pitchtools
        result = list(mathtools.difference_series(self.pitches))
        result = [-x for x in result]
        return pitchtools.NamedHarmonicIntervalSegment(result)

    @property
    def inflection_point_count(self):
        return len(self.local_minima) + len(self.local_maxima)

    @property
    def inversion_equivalent_chromatic_interval_class_segment(self):
        from abjad.tools import pitchtools
        pitch_classes = self.pitch_class_segment
        interval_classes = mathtools.difference_series(pitch_classes)
        return pitchtools.NumberedInversionEquivalentIntervalClassSegment(
            interval_classes)

    @property
    def inversion_equivalent_chromatic_interval_class_set(self):
        from abjad.tools import pitchtools
        pitch_classes = self.pitch_class_segment
        interval_classes = mathtools.difference_series(pitch_classes)
        return pitchtools.NumberedInversionEquivalentIntervalClassSet(
            interval_classes)

    @property
    def inversion_equivalent_chromatic_interval_class_vector(self):
        from abjad.tools import pitchtools
        pitch_classes = self.pitch_class_segment
        interval_classes = mathtools.difference_series(pitch_classes)
        return pitchtools.NumberedInversionEquivalentIntervalClassVector(
            interval_classes)

    @property
    def local_maxima(self):
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i-1], self[i], self[i+1]
                if left < middle and right < middle:
                    result.append(middle)
        return tuple(result)

    @property
    def local_minima(self):
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i-1], self[i], self[i+1]
                if middle < left and middle < right:
                    result.append(middle)
        return tuple(result)

    @property
    def melodic_chromatic_interval_class_segment(self):
        return [x.melodic_chromatic_interval_class 
            for x in self.melodic_chromatic_interval_segment]

    @property
    def melodic_chromatic_interval_segment(self):
        from abjad.tools import pitchtools
        result = list(
            mathtools.difference_series(self.chromatic_pitch_numbers))
        return pitchtools.NumberedMelodicIntervalSegment(result)

    @property
    def melodic_diatonic_interval_class_segment(self):
        return [x.melodic_diatonic_interval_class 
            for x in self.melodic_diatonic_interval_segment]

    @property
    def melodic_diatonic_interval_segment(self):
        from abjad.tools import pitchtools
        result = list(
            mathtools.difference_series(self.named_chromatic_pitches))
        result = [-x for x in result]
        return pitchtools.NamedMelodicIntervalSegment(result)

    @property
    def named_chromatic_pitch_class_vector(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedChromaticPitchClassVector(
            [pitch.pitch_class for pitch in self])

    @property
    def named_chromatic_pitch_set(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchSet(self[:])

    @property
    def named_chromatic_pitch_vector(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchVector(self.pitches)

    @property
    def named_chromatic_pitches(self):
        return self[:]

    @property
    def numbered_chromatic_pitch_class_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClassSegment(
            [pitch.pitch_class for pitch in self])

    @property
    def numbered_chromatic_pitch_class_set(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClassSet(
            [pitch.pitch_class for pitch in self])

    ### PUBLIC METHODS ###

    def transpose(self, melodic_interval):
        r'''Transpose pitches in pitch segment by melodic interval
        and emit new pitch segment.
        '''
        pitches = [pitch + melodic_interval for pitch in self]
        return type(self)(pitches)