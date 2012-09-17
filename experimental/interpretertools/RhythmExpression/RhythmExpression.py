from abjad.tools import durationtools
from abjad.tools.containertools.Container import Container


class RhythmExpression(Container):
    r'''.. versionadded:: 1.0

    Rhythm expression.

    One voice of counttime components: tuplets, notes, rests and chords.

    The interpretive process of building up the rhythm for a complete
    voice of music involves the generation of many different rhythm expressions.
    The rhythmic interpretation of a voice completes when enough    
    contiguous rhythm expressions exist to account for the entire
    duration of the voice.

    The many different rhythm expressions that together constitute the
    rhythm of a voice may not necessarily be constructed in
    chronological order during interpretation.

    Initializing ``start_offset=None`` will set `start_offset` to
    ``Offset(0)``.
    
    Composers do not create rhythm expression objects because 
    rhythm expressions arise as a byproduct of interpretation.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_forced_start_offset', )

    ### INITIALIZER ###

    def __init__(self, music=None, start_offset=None):
        Container.__init__(self, music=music)
        self._forced_start_offset = start_offset or durationtools.Offset(0)

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        new = Container.__copy__(self, *args)
        new._forced_start_offset = self.start_offset
        return new

    def __repr__(self):
        return '{}({}, start_offset={!r}, stop_offset={!r}'.format(
            self._class_name, Container.__repr__(self),
            self.start_offset, self.stop_offset)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        '''Rhythm expression start offset.

        Assigned at initialization during rhythm interpretation.

        Return offset.
        '''
        return self._forced_start_offset

    @property
    def stop_offset(self):
        '''Rhythm expression stop offset.
        
        Defined equal to start offset plus prolated duration.

        Return offset.
        '''
        return self.start_offset + self.prolated_duration
