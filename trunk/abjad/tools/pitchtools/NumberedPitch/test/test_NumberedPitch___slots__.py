# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NumberedPitch___slots___01():
    r'''Numbered chromatic pitches are immutable.
    '''

    numbered_chromatic_pitch = pitchtools.NumberedPitch(13)
    assert py.test.raises(AttributeError, "numbered_chromatic_pitch.foo = 'bar'")