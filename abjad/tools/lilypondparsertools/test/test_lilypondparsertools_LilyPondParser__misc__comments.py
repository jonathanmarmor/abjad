# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__misc__comments_01():
    r'''Comments are ignored.
    '''

    target = Staff()
    input = r'''\new Staff { %{ HOO HAH %} }'''
    parser = LilyPondParser()
    result = parser(input)
    assert format(target) == format(result) and target is not result
