# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import marktools
from abjad.tools import scoretools
from abjad.tools import marktools
from abjad.tools import scoretools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.abctools import AbjadObject
from abjad.tools.functiontools import attach


class GuileProxy(AbjadObject):
    r'''Emulates LilyPond music functions.

    Used internally by LilyPondParser.

    Not composer-safe.
    '''

    ### INITIALIZER ###

    def __init__(self, client):
        self.client = client

    ### SPECIAL METHODS ###

    def __call__(self, function_name, args):
        if hasattr(self, function_name[1:]):
            result = getattr(self, function_name[1:])(*args)
            return result
        message = "LilyPondParser can't emulate music function %s."
        raise Exception(message % function_name)

    ### FUNCTION EMULATORS ###

    def acciaccatura(self, music):
        grace = scoretools.GraceContainer(music[:])
        grace.kind = 'acciaccatura'
        return grace

    # afterGrace

    def appoggiatura(self, music):
        grace = scoretools.GraceContainer(music[:])
        grace.kind = 'appoggiatura'
        return grace

    def bar(self, string):
        return marktools.BarLine(string)

    def breathe(self):
        return marktools.LilyPondCommandMark('breathe', 'after')

    def clef(self, string):
        return marktools.ClefMark(string)

    def grace(self, music):
        return scoretools.GraceContainer(music[:])

    def key(self, notename_pitch, number_list):
        if number_list is None:
            number_list = 'major'
        return marktools.KeySignatureMark(notename_pitch, number_list)

    def language(self, string):
        if string in self.client._language_pitch_names:
            self.client._pitch_names = \
                self.client._language_pitch_names[string]
        # try reparsing the next note name, if a note name immediately follows
        lookahead = self.client._parser.lookahead
        if lookahead.type == 'STRING':
            if lookahead.value in self.client._pitch_names:
                lookahead.type = 'NOTENAME_PITCH'
                lookahead.value = self.client._pitch_names[lookahead.value]

    def makeClusters(self, music):
        return scoretools.Cluster(music[:])

    def mark(self, label):
        if label is None:
            label = '\default'
        return marktools.LilyPondCommandMark('mark %s' % label)

    def one_voice(self):
        return marktools.LilyPondCommandMark('oneVoice')

    # pitchedTrill

    def relative(self, pitch, music):
        # We should always keep track of the last chord entered.
        # When there are repeated chords (via q),
        # we add the last chord as a key in a _repeated_chords dictionary.
        # Then, we associate a list with the chord "key" in the dict,
        # and append a reference to the repeated chord.

        # Should the referenced chord appear in a relative block,
        # we relativize that chord, and update any repeated chords
        # we've added to its list of referencing chords.

        # The parser's "last_chord" variable will now reflect the
        # relativized pitches of the original referenced chord,
        # and so any new chord repetitions following the \relative block
        # should result in matching absolute pitches to both the "last_chord"
        # and any other repetitions.

        if self._is_unrelativable(music):
            return music

        def recurse(component, pitch):
            if self._is_unrelativable(component):
                return pitch
            elif isinstance(component, (scoretools.Chord, scoretools.Note)):
                pitch = self._make_relative_leaf(component, pitch)
                if component in self.client._repeated_chords:
                    for repeated_chord in \
                        self.client._repeated_chords[component]:
                        repeated_chord.written_pitches = \
                            component.written_pitches
            elif isinstance(component, scoretools.Container):
                for child in component:
                    pitch = recurse(child, pitch)
            return pitch

        pitch = recurse(music, pitch)

        self._make_unrelativable(music)

        return music

    def skip(self, duration):
        leaf = scoretools.Skip(duration.duration)
        if duration.multiplier is not None:
            leaf.lilypond_duration_multiplier = duration.multiplier
        return leaf

    def slashed_grace_container(self, music):
        grace = scoretools.GraceContainer(music[:])
        grace.kind = 'slashedGrace'
        return grace

    def time(self, number_list, fraction):
        n, d = fraction.numerator, fraction.denominator
        return marktools.TimeSignatureMark(
            (n, d), target_context=scoretools.Staff)

    def times(self, fraction, music):
        n, d  = fraction.numerator, fraction.denominator
        if not isinstance(music, scoretools.Context) and \
            not isinstance(music, scoretools.Leaf):
            return scoretools.Tuplet((n, d), music[:])
        return scoretools.Tuplet((n, d), [music])

    def transpose(self, from_pitch, to_pitch, music):
        from abjad.tools import lilypondparsertools
        self._make_unrelativable(music)
        def recurse(music):
            key_signatures = music._get_marks(marktools.KeySignatureMark)
            if key_signatures:
                for x in key_signatures:
                    tonic = pitchtools.NamedPitch(x.tonic, 4)
                    x.tonic = lilypondparsertools.LilyPondParser._transpose_enharmonically(
                        from_pitch, to_pitch, tonic).named_pitch_class
            if isinstance(music, scoretools.Note):
                music.written_pitch = \
                    lilypondparsertools.LilyPondParser._transpose_enharmonically(
                    from_pitch, to_pitch, music.written_pitch)
            elif isinstance(music, scoretools.Chord):
                for note_head in music.note_heads:
                    note_head.written_pitch = \
                        lilypondparsertools.LilyPondParser._transpose_enharmonically(
                        from_pitch, to_pitch, note_head.written_pitch)
            elif isinstance(music, scoretools.Container):
                for x in music:
                    recurse(x)
        recurse(music)
        return music

    # transposition

    # tweak

    def voiceFour(self):
        return marktools.LilyPondCommandMark('voiceTwo')

    def voiceOne(self):
        return marktools.LilyPondCommandMark('voiceOne')

    def voiceThree(self):
        return marktools.LilyPondCommandMark('voiceThree')

    def voiceTwo(self):
        return marktools.LilyPondCommandMark('voiceFour')

    ### HELPER FUNCTIONS ###

    def _is_unrelativable(self, music):
        annotations = music._get_marks(marktools.Annotation)
        if 'UnrelativableMusic' in [x.name for x in annotations]:
            return True
        return False

    def _make_relative_leaf(self, leaf, pitch):
        if self._is_unrelativable(leaf):
            return pitch
        elif isinstance(leaf, scoretools.Note):
            pitch = self._to_relative_octave(leaf.written_pitch, pitch)
            leaf.written_pitch = pitch
        elif isinstance(leaf, scoretools.Chord):
            # TODO: This is not ideal w/r/t post events as LilyPond does 
            # not sort chord contents
            chord_pitches = self.client._chord_pitch_orders[leaf]
            for i, chord_pitch in enumerate(chord_pitches):
                pitch = self._to_relative_octave(chord_pitch, pitch)
                chord_pitches[i] = pitch
            leaf.written_pitches = chord_pitches
            pitch = min(leaf.written_pitches)
        return pitch

    def _make_unrelativable(self, music):
        if not self._is_unrelativable(music):
            annotation = marktools.Annotation('UnrelativableMusic')
            attach(annotation, music)

    def _to_relative_octave(self, pitch, reference):
        if pitch.pitch_class_number > \
            reference.pitch_class_number:
            up_pitch = pitchtools.NamedPitch(
                pitch.pitch_class_name, reference.octave_number)
            down_pitch = pitchtools.NamedPitch(
                pitch.pitch_class_name, reference.octave_number - 1)
            up_octave, down_octave = \
                up_pitch.octave_number, down_pitch.octave_number
        else:
            up_pitch = pitchtools.NamedPitch(
                pitch.pitch_class_name, reference.octave_number + 1)
            down_pitch = pitchtools.NamedPitch(
                pitch.pitch_class_name, reference.octave_number)
            up_octave, down_octave = \
                up_pitch.octave_number, down_pitch.octave_number
        if abs(
                float(up_pitch.diatonic_pitch_number) - 
                float(reference.diatonic_pitch_number)) < \
            abs(
                float(down_pitch.diatonic_pitch_number) - 
                float(reference.diatonic_pitch_number)):
            pitch = pitchtools.NamedPitch(
                up_pitch.named_pitch_class, 
                up_octave + pitch.octave_number - 3)
        else:
            pitch = pitchtools.NamedPitch(
                down_pitch.named_pitch_class, 
                down_octave + pitch.octave_number - 3)
        return pitch