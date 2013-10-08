# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_pitch_name_to_diatonic_pitch_number_01():

    assert pitchtools.pitch_name_to_diatonic_pitch_number("cf''") == 7
    assert pitchtools.pitch_name_to_diatonic_pitch_number("c''") == 7
    assert pitchtools.pitch_name_to_diatonic_pitch_number("cs''") == 7
    assert pitchtools.pitch_name_to_diatonic_pitch_number("bf''") == 13
    assert pitchtools.pitch_name_to_diatonic_pitch_number("b''") == 13
    assert pitchtools.pitch_name_to_diatonic_pitch_number("bs''") == 13