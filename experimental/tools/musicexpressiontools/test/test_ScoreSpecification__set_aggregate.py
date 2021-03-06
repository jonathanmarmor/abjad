# -*- encoding: utf-8 -*-
from experimental import *


def test_ScoreSpecification__set_aggregate_01():
    r'''Register according to example aggregate 0.
    '''

    score_template = templatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
#    rhythm = new(
#        library.sixteenths,
#        beam_divisions_together=False,
#        )
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    score_specification.select_leaves('Voice 1').set_pitch(library.example_pitches_1())
    score_specification.select_leaves('Voice 1').set_aggregate(library.example_aggregates[0])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_aggregate_02():
    r'''Register according to example aggregate 1.
    '''

    score_template = templatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
#    rhythm = new(
#        library.sixteenths,
#        beam_divisions_together=False,
#        )
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    score_specification.select_leaves('Voice 1').set_pitch(library.example_pitches_1())
    score_specification.select_leaves('Voice 1').set_aggregate(library.example_aggregates[1])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
