# -*- encoding: utf-8 -*-
import pytest
from experimental import *


def test_SegmentSpecification__set_rhythm_from_parseable_string_01():

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 8), (3, 8)])
    red_segment.set_rhythm("{ c'16 [ ( c'8 c'8. ] ) }")
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(
        score,
        __file__,
        current_function_name,
        )
    assert format(score) == systemtools.TestManager.read_test_output(
        __file__,
        current_function_name,
        )


def test_SegmentSpecification__set_rhythm_from_parseable_string_02():
    r'''Reflect material.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    material_manager = musicexpressiontools.MaterialManager()
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 8), (3, 8)])
    rhythm = material_manager.register_material("{ c'16 [ ( c'8 c'8. ] ) }")
    red_segment.set_rhythm(rhythm.reflect())
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(
        score,
        __file__,
        current_function_name,
        )
    assert format(score) == systemtools.TestManager.read_test_output(
        __file__,
        current_function_name,
        )
