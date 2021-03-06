# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSelectExpression__divide_by_ratio_01():

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    second_half_of_segment = red_segment.timespan.divide_by_ratio((1, 1))[-1]
    red_segment.set_divisions([(2, 16)])
    second_half_of_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSelectExpression__divide_by_ratio_02():

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_third_of_segment = red_segment.timespan.divide_by_ratio((1, 1, 1))[1]
    red_segment.set_divisions([(2, 16)])
    middle_third_of_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSelectExpression__divide_by_ratio_03():
    r'''One-segment score.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    divisions = red_segment.timespan.divide_by_ratio([1, 1, 1])
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.joined_sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSelectExpression__divide_by_ratio_04():
    r'''Two-segment score.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    divisions = red_segment.timespan.divide_by_ratio([1, 1, 1])
    red_segment.set_divisions(divisions)
    red_segment.set_rhythm(library.joined_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
