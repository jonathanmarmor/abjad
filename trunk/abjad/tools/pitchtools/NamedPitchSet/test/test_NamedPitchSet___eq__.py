# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitchSet___eq___01():
    r'''Pitch set equality works as expected.
    '''

    pset1 = pitchtools.NamedPitchSet([12, 14, 18, 19])
    pset2 = pitchtools.NamedPitchSet([12, 14, 18, 19])
    pset3 = pitchtools.NamedPitchSet([12, 14, 18, 20])

    assert pset1 == pset2
    assert pset1 != pset3
    assert pset2 != pset3
    assert not pset1 != pset2