from experimental import *
import py


def test_Session_command_repetition_01():
    py.test.skip('TODO: command repetition is currently broken.')

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='next . . . q')
    assert score_manager.session.command_history == ['next', '.', '.', '.', 'q']
    assert score_manager.session.io_transcript.signature == (10, (1, 3, 5, 7))