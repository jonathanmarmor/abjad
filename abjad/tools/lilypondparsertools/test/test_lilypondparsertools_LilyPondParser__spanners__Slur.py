# -*- encoding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__Slur_01():
    r'''Successful slurs, showing single leaf overlap.
    '''

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    slur = Slur()
    attach(slur, target[2:])
    slur = Slur()
    attach(slur, target[:3])

    assert systemtools.TestManager.compare(
        target,
        r'''
        {
            c'4 (
            c'4
            c'4 ) (
            c'4 )
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Slur_02():
    r'''Swapped start and stop.
    '''

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    slur = Slur()
    attach(slur, target[2:])
    slur = Slur()
    attach(slur, target[:3])

    assert systemtools.TestManager.compare(
        target,
        r'''
        {
            c'4 (
            c'4
            c'4 ) (
            c'4 )
        }
        '''
        )

    string = r"\relative c' { c ( c c () c ) }"

    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Slur_03():
    r'''Single leaf.
    '''

    string = '{ c () c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Slur_04():
    r'''Unterminated.
    '''

    string = '{ c ( c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Slur_05():
    r'''Unstarted.
    '''

    string = '{ c c c c ) }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Slur_06():
    r'''Nested.
    '''

    string = '{ c ( c ( c ) c ) }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Slur_07():
    r'''With direction.
    '''

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    slur = Slur(direction=Down)
    attach(slur, target[:3])
    slur = Slur(direction=Up)
    attach(slur, target[2:])

    assert systemtools.TestManager.compare(
        target,
        r'''
        {
            c'4 _ (
            c'4
            c'4 ) ^ (
            c'4 )
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
