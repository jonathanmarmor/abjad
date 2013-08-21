# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_deviation_in_cents_01():
    r'''Deviation defaults to None.
    '''

    pitch = pitchtools.NamedPitch('bf', 2)
    assert pitch.deviation_in_cents is None


def test_NamedPitch_deviation_in_cents_02():
    r'''Deviation can be int or float.
    '''

    pitch = pitchtools.NamedPitch('bf', 4, -31)
    assert pitch.deviation_in_cents == -31

    pitch = pitchtools.NamedPitch('bf', 4, -12.4)
    assert pitch.deviation_in_cents == -12.4