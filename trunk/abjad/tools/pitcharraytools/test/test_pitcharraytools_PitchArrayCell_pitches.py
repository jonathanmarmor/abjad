# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import pitcharraytools
from abjad.tools.pitcharraytools import PitchArrayCell


def test_pitcharraytools_PitchArrayCell_pitches_01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(pitchtools.NamedPitch(0))
    array[0].cells[1].pitches.append(pitchtools.NamedPitch(2))

    '''
    [c'] [d'     ] []
    [         ] [] []
    '''

    assert array[0].cells[0].pitches == [pitchtools.NamedPitch(0)]
    assert array[0].cells[1].pitches == [pitchtools.NamedPitch(2)]
    assert array[0].cells[2].pitches == []

    assert array[1].cells[0].pitches == []
    assert array[1].cells[1].pitches == []
    assert array[1].cells[2].pitches == []


def test_pitcharraytools_PitchArrayCell_pitches_02():

    cell = PitchArrayCell([pitchtools.NamedPitch(0)])

    assert cell.pitches == [pitchtools.NamedPitch(0)]