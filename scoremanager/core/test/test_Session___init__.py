# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session___init___01():
    r'''Attributes assigned at initialization time.
    '''

    session = scoremanager.core.Session()

    assert session.initial_user_input is None
    assert session._breadcrumb_stack == []
    assert session.scores_to_show == 'active'
    assert session.pending_user_input is None
