from abjad import *
from abjad.tools import tonalanalysistools


def test_SuspensionIndicator__init_by_start_and_stop_01():

    t = tonalanalysistools.SuspensionIndicator(4, 3)

    assert t.start == tonalanalysistools.ScaleDegree(4)
    assert t.stop == tonalanalysistools.ScaleDegree(3)


def test_SuspensionIndicator__init_by_start_and_stop_02():

    t = tonalanalysistools.SuspensionIndicator(4, ('flat', 3))

    assert t.start == tonalanalysistools.ScaleDegree(4)
    assert t.stop == tonalanalysistools.ScaleDegree('flat', 3)