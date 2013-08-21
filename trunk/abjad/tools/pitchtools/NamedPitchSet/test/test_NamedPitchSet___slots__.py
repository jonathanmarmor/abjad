# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NamedPitchSet___slots___01():
    r'''Named chromatic pitch sets are immutable.
    '''

    ncps = ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    named_chromatic_pitch_set = pitchtools.NamedPitchSet(ncps)

    assert py.test.raises(AttributeError, "named_chromatic_pitch_set.foo = 'bar'")