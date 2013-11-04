# -*- encoding: utf-8 -*-
import copy
import re
from abjad.tools.scoretools.Leaf import Leaf


class Chord(Leaf):
    r'''A chord.

    ..  container:: example

        **Example.**

        ::

            >>> chord = Chord("<e' cs'' f''>4")
            >>> show(chord) # doctest: +SKIP

        ..  doctest::

            >>> f(chord)
            <e' cs'' f''>4

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_note_heads',
        '_written_pitches',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import lilypondparsertools
        from abjad.tools import scoretools
        self._note_heads = scoretools.NoteHeadInventory(
            client=self,
            )
        if len(args) == 1 and isinstance(args[0], str):
            input = '{{ {} }}'.format(args[0])
            parsed = lilypondparsertools.LilyPondParser()(input)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            args = [parsed[0]]
        is_cautionary = []
        is_forced = []
        if len(args) == 1 and isinstance(args[0], Leaf):
            leaf = args[0]
            written_duration = leaf.written_duration
            lilypond_multiplier = leaf.lilypond_duration_multiplier
            if hasattr(leaf, 'written_pitch'):
                written_pitches = [leaf.written_pitch]
                is_cautionary = [leaf.note_head.is_cautionary]
                is_forced = [leaf.note_head.is_forced]
            elif hasattr(leaf, 'written_pitches'):
                written_pitches = leaf.written_pitches
                is_cautionary = [x.is_cautionary for x in leaf.note_heads]
                is_forced = [x.is_forced for x in leaf.note_heads]
            else:
                written_pitches = []
            self._copy_override_and_set_from_leaf(leaf)
        elif len(args) == 2:
            written_pitches, written_duration = args
            if isinstance(written_pitches, str):
                written_pitches = [x for x in written_pitches.split() if x]
            lilypond_multiplier = None
        elif len(args) == 3:
            written_pitches, written_duration, lilypond_multiplier = args
        else:
            message = 'can not initialize chord from {!r}.'.format(args)
            raise ValueError(message)
        Leaf.__init__(self, written_duration, lilypond_multiplier)
        if not is_cautionary:
            is_cautionary = [False] * len(written_pitches)
        if not is_forced:
            is_forced = [False] * len(written_pitches)
        for written_pitch, cautionary, forced in zip(
            written_pitches, is_cautionary, is_forced):
            note_head = scoretools.NoteHead(
                written_pitch=written_pitch,
                is_cautionary=cautionary,
                is_forced=forced,
                )
            self._note_heads.append(note_head)

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        '''Gets new arguments.

        Returns tuple.
        '''
        result = []
        result.append(self.written_pitches)
        result.extend(Leaf.__getnewargs__(self))
        return tuple(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        return '<%s>%s' % (self._summary, self._formatted_duration)

    @property
    def _summary(self):
        return ' '.join([str(x) for x in self.note_heads])

    ### PRIVATE METHODS ###

    @staticmethod
    def _cast_defective_chord(chord):
        from abjad.tools import scoretools
        if isinstance(chord, Chord):
            note_head_count = len(chord.note_heads)
            if not note_head_count:
                return scoretools.Rest(chord)
            elif note_head_count == 1:
                return scoretools.Note(chord)
        return chord

    def _copy_with_marks_but_without_children_or_spanners(self):
        new = Leaf._copy_with_marks_but_without_children_or_spanners(self)
        new.note_heads[:] = []
        for note_head in self.note_heads:
            new_note_head = copy.copy(note_head)
            new.note_heads.append(new_note_head)
        return new

    def _divide(self, pitch=None):
        from abjad.tools import scoretools
        from abjad.tools import markuptools
        from abjad.tools import pitchtools
        pitch = pitch or pitchtools.NamedPitch('b', 3)
        pitch = pitchtools.NamedPitch(pitch)
        treble = copy.copy(self)
        bass = copy.copy(self)
        for mark in treble._get_marks(mark_classes=markuptools.Markup):
            mark.detach()
        for mark in bass._get_marks(mark_classes=markuptools.Markup):
            mark.detach()

        if isinstance(treble, scoretools.Note):
            if treble.written_pitch < pitch:
                treble = scoretools.Rest(treble)
        elif isinstance(treble, scoretools.Rest):
            pass
        elif isinstance(treble, scoretools.Chord):
            for note_head in reversed(treble.note_heads):
                if note_head.written_pitch < pitch:
                    treble.note_heads.remove(note_head)
        else:
            raise TypeError

        if isinstance(bass, scoretools.Note):
            if pitch <= bass.written_pitch:
                bass = scoretools.Rest(bass)
        elif isinstance(bass, scoretools.Rest):
            pass
        elif isinstance(bass, scoretools.Chord):
            for note_head in reversed(bass.note_heads):
                if pitch <= note_head.written_pitch:
                    bass.note_heads.remove(note_head)
        else:
            raise TypeError

        treble = self._cast_defective_chord(treble)
        bass = self._cast_defective_chord(bass)

        up_markup = self._get_markup(direction=Up)
        up_markup = [copy.copy(markup) for markup in up_markup]

        down_markup = self._get_markup(direction=Down)
        down_markup = [copy.copy(markup) for markup in down_markup]

        for markup in up_markup:
            markup(treble)
        for markup in down_markup:
            markup(bass)

        return treble, bass

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        r'''LilyPond format of chord.

        ..  container:: example

            **Example.**

            ::

                >>> chord = Chord("<e' cs'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> chord.lilypond_format
                "<e' cs'' f''>4"

        Returns string.
        '''
        return super(Chord, self).lilypond_format

    @apply
    def note_heads():
        def fget(self):
            r'''Note heads in chord.

            ..  container:: example

                **Example 1.** Get note heads in chord:

                ::

                    >>> chord = Chord("<g' c'' e''>4")
                    >>> show(chord) # doctest: +SKIP

                ::

                    >>> print chord.note_heads.storage_format
                    scoretools.NoteHeadInventory([
                        scoretools.NoteHead(
                            written_pitch=pitchtools.NamedPitch("g'"),
                            is_cautionary=False,
                            is_forced=False
                            ),
                        scoretools.NoteHead(
                            written_pitch=pitchtools.NamedPitch("c''"),
                            is_cautionary=False,
                            is_forced=False
                            ),
                        scoretools.NoteHead(
                            written_pitch=pitchtools.NamedPitch("e''"),
                            is_cautionary=False,
                            is_forced=False
                            ),
                        ],
                        client=scoretools.Chord(),
                        )

            ..  container:: example

                **Example 2.** Set note heads with pitch names:

                ::

                    >>> chord = Chord("<g' c'' e''>4")
                    >>> show(chord) # doctest: +SKIP

                ::

                    >>> chord.note_heads = "c' d' fs'"
                    >>> show(chord) # doctest: +SKIP

                ..  doctest::

                    >>> f(chord)
                    <c' d' fs'>4

            ..  container:: example

                **Example 3.** Set note heads with pitch numbers:

                    >>> chord = Chord("<g' c'' e''>4")
                    >>> show(chord) # doctest: +SKIP

                ::

                    >>> chord.note_heads = [16, 17, 19]
                    >>> show(chord) # doctest: +SKIP

                ..  doctest::

                    >>> f(chord)
                    <e'' f'' g''>4

            Set note heads with any iterable.

            Returns tuple.
            '''
            return self._note_heads
        def fset(self, note_heads):
            self._note_heads[:] = []
            if isinstance(note_heads, str):
                note_heads = note_heads.split()
            self.note_heads.extend(note_heads)
        return property(**locals())

    @property
    def override(self):
        r'''LilyPond grob override component plug-in.

        ..  container:: example

            **Example.** Override LilyPond accidental, note head and stem
            grobs:

            ::

                >>> chord = Chord("<e' cs'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> override(chord).accidental.color = 'red'
                >>> override(chord).note_head.color = 'red'
                >>> override(chord).stem.color = 'red'
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                \once \override Accidental #'color = #red
                \once \override NoteHead #'color = #red
                \once \override Stem #'color = #red
                <e' cs'' f''>4

        Returns none.
        '''
        return super(Chord, self).override

    @property
    def set(self):
        r'''LilyPond context setting component plug-in.

        ..  container:: example

            **Example.** Set LilyPond ``stemLeftBeamCount``
            and ``stemRightBeamCount`` context settings:

            ::

                >>> chord = Chord("<e' cs'' f''>16")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> beam = spannertools.BeamSpanner()
                >>> attach(beam, [chord])
                >>> chord.set.stem_left_beam_count = 0
                >>> chord.set.stem_right_beam_count = 2
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #2
                <e' cs'' f''>16 [ ]

        Returns none.
        '''
        return super(Chord, self).set

    @property
    def sounding_pitches(self):
        r"""Sounding pitches in chord.

        ..  container:: example

            **Example.**

            ::

                >>> staff = Staff("<c''' e'''>4 <d''' fs'''>4")
                >>> glockenspiel = instrumenttools.Glockenspiel()
                >>> glockenspiel = attach(glockenspiel, staff)
                >>> instrumenttools.transpose_from_sounding_pitch_to_written_pitch(
                ...     staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Glockenspiel }
                    \set Staff.shortInstrumentName = \markup { Gkspl. }
                    <c' e'>4
                    <d' fs'>4
                }

            ::

                >>> staff[0].sounding_pitches
                (NamedPitch("c'''"), NamedPitch("e'''"))

        Returns tuple.
        """
        from abjad.tools import instrumenttools
        from abjad.tools import pitchtools
        if self.written_pitch_indication_is_at_sounding_pitch:
            return self.written_pitches
        else:
            instrument = self._get_effective_context_mark(
                instrumenttools.Instrument)
            if not instrument:
                message = 'effective instrument of note can not be determined.'
                raise InstrumentError(message)
            sounding_pitch = instrument.sounding_pitch_of_written_middle_c
            interval = pitchtools.NamedPitch('C4') - sounding_pitch
            sounding_pitches = [
                pitchtools.transpose_pitch_carrier_by_interval(
                pitch, interval) for pitch in self.written_pitches]
            return tuple(sounding_pitches)

    @apply
    def written_duration():
        def fget(self):
            r'''Written duration of chord.

            ..  container:: example

                **Example 1.** Get written duration:

                ::

                    >>> chord = Chord("<e' cs'' f''>4")
                    >>> show(chord) # doctest: +SKIP

                ::

                    >>> chord.written_duration
                    Duration(1, 4)

            ..  container:: example

                **Example 2.** Set written duration:

                ::

                    >>> chord = Chord("<e' cs'' f''>4")
                    >>> show(chord) # doctest: +SKIP

                ::

                    >>> chord.written_duration = Duration(1, 16)
                    >>> show(chord) # doctest: +SKIP

            Set duration.

            Returns duration.
            '''
            return Leaf.written_duration.fget(self)
        def fset(self, expr):
            Leaf.written_duration.fset(self, expr)
        return property(**locals())

    @apply
    def written_pitches():
        def fget(self):
            r'''Written pitches in chord.

            ..  container:: example

                **Example 1.** Get written pitches:

                    >>> chord = Chord("<g' c'' e''>4")
                    >>> show(chord) # doctest: +SKIP

                ::

                    >>> for written_pitch in chord.written_pitches:
                    ...     written_pitch
                    NamedPitch("g'")
                    NamedPitch("c''")
                    NamedPitch("e''")

            ..  container:: example

                **Example 2.** Set written pitches with pitch names:

                ::

                    >>> chord = Chord("<e' g' c''>4")
                    >>> show(chord) # doctest: +SKIP

                ::

                    >>> chord.written_pitches = "f' b' d''"
                    >>> show(chord) # doctest: +SKIP

                ..  doctest::

                    >>> f(chord)
                    <f' b' d''>4

            Set written pitches with any iterable.

            Returns tuple.
            '''
            return tuple(note_head.written_pitch
                for note_head in self.note_heads)
        def fset(self, pitches):
            self.note_heads = pitches
        return property(**locals())

    ### PUBLIC METHODS ###

    def get_note_head(self, pitch):
        r'''Gets note head in chord by `pitch`.

        ..  container:: example

            **Example 1.** Get note head by pitch name:

            ::

                >>> chord = Chord("<e' cs'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> note_head = chord.get_note_head("e'")
                >>> note_head.tweak.color = 'red'
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                <
                    \tweak #'color #red
                    e'
                    cs''
                    f''
                >4

        ..  container:: example

            **Example 2.** Get note head by pitch number:

            ::

                >>> chord = Chord("<e' cs'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> note_head = chord.get_note_head(4)
                >>> note_head.tweak.color = 'red'
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                <
                    \tweak #'color #red
                    e'
                    cs''
                    f''
                >4

        Raises missing note head error when chord contains no
        note head with `pitch`.

        Raises extra note head error when chord contains more than
        one note head with `pitch`.

        Returns note head.
        '''
        from abjad.tools import pitchtools
        result = []
        pitch = pitchtools.NamedPitch(pitch)
        for note_head in self.note_heads:
            if note_head.written_pitch == pitch:
                result.append(note_head)
        count = len(result)
        if count == 0:
            raise MissingNoteHeadError
        elif count == 1:
            note_head = result[0]
            return note_head
        else:
            raise ExtraNoteHeadError
