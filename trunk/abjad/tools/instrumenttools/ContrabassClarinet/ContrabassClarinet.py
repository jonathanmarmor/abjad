# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Clarinet.Clarinet import Clarinet


class ContrabassClarinet(Clarinet):
    r'''Abjad model of the contrassbass clarinet:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.ContrabassClarinet()(staff)
        ContrabassClarinet()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Contrabass clarinet }
            \set Staff.shortInstrumentName = \markup { Cbass cl. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The contrabass clarinet targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Clarinet.__init__(self, **kwargs)
        self._default_instrument_name = 'contrabass clarinet'
        self._default_short_instrument_name = 'cbass cl.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedChromaticPitch('bf,,')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self.all_clefs = [
            contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._traditional_pitch_range = pitchtools.PitchRange(-38, 7)
