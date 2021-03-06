# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_instrument_name_markup_01():
    r'''Quit, back & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score score~setup instrumentation hornist horn im q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (13,)

    string = 'red~example~score score~setup instrumentation'
    string += ' hornist horn im b q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (15, (10, 13))

    string = 'red~example~score score~setup instrumentation'
    string += ' hornist horn im home q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (15, (0, 13))
