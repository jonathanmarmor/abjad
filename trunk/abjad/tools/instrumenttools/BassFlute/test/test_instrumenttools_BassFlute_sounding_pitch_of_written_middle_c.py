# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_BassFlute_sounding_pitch_of_written_middle_c_01():

    bass_flute = instrumenttools.BassFlute()

    assert bass_flute.sounding_pitch_of_written_middle_c == 'c'