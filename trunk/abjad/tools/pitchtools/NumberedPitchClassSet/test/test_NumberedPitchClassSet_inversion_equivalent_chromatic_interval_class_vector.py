# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSet_inversion_equivalent_chromatic_interval_class_vector_01():

    pcset = pitchtools.NumberedPitchClassSet([0, 6, 10, 4, 9, 2])
    icvector = pitchtools.NumberedInversionEquivalentIntervalClassVector([
        1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 6, 6])
    "IntervalClassVector(0 | 1 4 2 4 2 2)"

    assert pcset.inversion_equivalent_chromatic_interval_class_vector == icvector