# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
from scoremanager.iotools import Selector


def test_Selector_make_performer_selector_01():

    session = scoremanager.core.Session()
    session.snake_case_current_score_name = 'red_example_score'
    selector = Selector.make_performer_selector(session=session)
    result = selector._run(pending_user_input='hornist')

    performer = instrumenttools.Performer(
        name='hornist', 
        instruments=[instrumenttools.FrenchHorn()]
        )
    assert result == performer
