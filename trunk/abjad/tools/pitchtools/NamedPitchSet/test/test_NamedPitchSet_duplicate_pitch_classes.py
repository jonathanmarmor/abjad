# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitchSet_duplicate_pitch_classes_01():

    pset = pitchtools.NamedPitchSet([0, 12, 13, 26])

    assert pset.duplicate_pitch_classes == pitchtools.NumberedPitchClassSet([0])


def test_NamedPitchSet_duplicate_pitch_classes_02():

    pset = pitchtools.NamedPitchSet([0, 13, 26])

    assert pset.duplicate_pitch_classes == pitchtools.NumberedPitchClassSet([])