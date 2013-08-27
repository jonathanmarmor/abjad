# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedTuple import TypedTuple


class PitchSegment(TypedTuple):
    r'''Abjad model of a pitch segment:

    ::

        >>> numbered_pitch_segment = pitchtools.PitchSegment(
        ...     tokens=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=pitchtools.NumberedPitch,
        ...     )
        >>> numbered_pitch_segment
        PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

    ::

        >>> named_pitch_segment = pitchtools.PitchSegment(
        ...     ['bf,', 'aqs', "fs'", "g'", 'bqf', "g'"],
        ...     item_class=pitchtools.NamedPitch,
        ...     )
        >>> named_pitch_segment
        PitchSegment(['bf,', 'aqs', "fs'", "g'", 'bqf', "g'"])

    Return pitch segment.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        [-2, -1.5, 6, 7, -1.5, 7],
        )

    __slots__ = ()
    
    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools 
        assert item_class in (
            None,
            pitchtools.NamedPitch,
            pitchtools.NumberedPitch,
            )
        if item_class is None:
            item_class = pitchtools.NumberedPitch
        TypedTuple.__init__(
            self,
            tokens=tokens,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}([{}])'.format(self._class_name, self._repr_string)

    def __str__(self):
        return '<{}>' % self._format_string
        
    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        from abjad.tools import pitchtools
        parts = []
        if self.item_class is pitchtools.NamedPitch:
            parts = [repr(str(x)) for x in self]
        else:
            parts = [str(x) for x in self]
        return ', '.join(parts)

    @property
    def _repr_string(self):
        return self._format_string

    ### PUBLIC PROPERTIES ###

    @property
    def inflection_point_count(self):
        return len(self.local_minima) + len(self.local_maxima)

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

    ### PUBLIC METHODS ###

    def invert(self, axis):
        r'''Invert pitch segment around `axis`.

        Emit new pitch segment.
        '''
        tokens = (pitch.invert(axis) for pitch in self)
        return self.new(tokens=tokens)

    def is_equivalent_under_transposition(self, expr):
        r'''True if equivalent under transposition to `expr`, otherwise False.
        
        Return boolean.
        '''
        from abjad.tools import pitchtools
        if not isinstance(expr, type(self)):
            return False
        if not len(self) == len(expr):
            return False
        difference = -(pitchtools.NamedPitch(expr[0], 4) -
            pitchtools.NamedPitch(self[0], 4))
        new_pitches = (x + difference for x in self)
        new_pitches = self.new(tokens=new_pitch)
        return arg == new_pitches

    def make_notes(self, n=None, written_duration=None):
        r'''Make first `n` notes in pitch class segment.

        Set `n` equal to `n` or length of segment.

        Set `written_duration` equal to `written_duration` or ``1/8``:

        ::

            >>> notes = named_pitch_segment.make_notes()
            >>> staff = Staff(notes)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                bf,8
                aqs8
                fs'8
                g'8
                bqf8
                g'8
            }

        Allow nonassignable `written_duration`:

        ::

            >>> notes = named_pitch_segment.make_notes(4, Duration(5, 16))
            >>> staff = Staff(notes)
            >>> time_signature = contexttools.TimeSignatureMark((5, 4))(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest:: 

            >>> f(staff)
            \new Staff {
                \time 5/4
                bf,4 ~
                bf,16
                aqs4 ~
                aqs16
                fs'4 ~
                fs'16
                g'4 ~
                g'16
            }

        Return list of notes.
        '''
        from abjad.tools import durationtools
        from abjad.tools import iterationtools
        from abjad.tools import notetools
        from abjad.tools import pitchtools
        n = n or len(self)
        written_duration = written_duration or durationtools.Duration(1, 8)
        result = notetools.make_notes([0] * n, [written_duration])
        for i, tie_chain in enumerate(
            iterationtools.iterate_tie_chains_in_expr(result)):
            pitch = self[i % len(self)]
            for note in tie_chain:
                note.written_pitch = pitch
        return result

    def retrograde(self):
        r'''Retrograde of pitch segment:

        ::

            >>> named_pitch_segment.retrograde()
            PitchSegment(["g'", 'bqf', "g'", "fs'", 'aqs', 'bf,'])

        Emit new pitch segment.
        '''
        return self.new(tokens=reversed(self))

    def rotate(self, n):
        r'''Rotate pitch segment:

        ::

            >>> numbered_pitch_segment.rotate(1)
            PitchSegment([7, -2, -1.5, 6, 7, -1.5])

        ::

            >>> named_pitch_segment.rotate(-2) 
            PitchSegment(["fs'", "g'", 'bqf', "g'", 'bf,', 'aqs'])

        Emit new pitch segment.
        '''
        from abjad.tools import sequencetools
        tokens = sequencetools.rotate_sequence(self._collection, n)
        return self.new(tokens=tokens)

    def transpose(self, expr):
        r'''Transpose pitch segment by `expr`.

        Emit new pitch segment.
        '''
        tokens = (pitch.transpose(expr) for pitch in self)
        return self.new(tokens=tokens) 