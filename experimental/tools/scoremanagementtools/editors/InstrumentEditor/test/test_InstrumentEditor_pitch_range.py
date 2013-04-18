from abjad import *
from experimental import *


def test_InstrumentEditor_pitch_range_01():

    editor = scoremanagementtools.editors.InstrumentEditor()
    editor.run(user_input='marimba q')
    assert editor.target.pitch_range == pitchtools.PitchRange(-19, 36)

    editor = scoremanagementtools.editors.InstrumentEditor()
    editor.run(user_input='marimba rg [C2, C7] q')
    assert editor.target.pitch_range == pitchtools.PitchRange(-24, 36)