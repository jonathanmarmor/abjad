# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Contrabass_sounding_pitch_of_written_middle_c_01():

    contrabass = instrumenttools.Contrabass()

    assert contrabass.sounding_pitch_of_written_middle_c == 'c'