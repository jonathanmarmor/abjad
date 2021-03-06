# -*- encoding: utf-8 -*-
from experimental import *


def test_multiple_segment_solo_01():
    r'''Single division interprets cyclically over two segments.
    Division does not truncate at segment boundary.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_02():
    r'''Single division interprets cyclically over two segments.
    Division truncates at segment boundary because of truncate keyword.
    Division starts over at beginning of second segment.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], truncate=True)
    red_segment.set_rhythm(library.joined_thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_03():
    r'''Single division exactly equal to duration of single segment.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(14, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_04():
    r'''Single division exactly equal to duration of single segment.
    Division truncates because truncate keyword is set to true.
    Division starts over at beginning of second segment.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(14, 16)], contexts=['Voice 1'], truncate=True)
    red_segment.set_rhythm(library.joined_thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_05():
    r'''Single division greater in duration than single segment but lesser in duration than two segments.
    Division does not truncate at segment boundary.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(20, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_06():
    r'''Single division greater in duration than single segment but lesser in duration than two segments.
    Division truncates at segment boundary because truncate keyword is set to true.
    Division starts over from beginning of second segment.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(20, 16)], contexts=['Voice 1'], truncate=True)
    red_segment.set_rhythm(library.joined_thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_07():
    r'''Large division greater in duration than two segments.
    Division does not truncate at segment boundaries.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(15, 8)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    green_segment = score_specification.append_segment(name='green')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
