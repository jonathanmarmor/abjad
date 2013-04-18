from experimental import *


def test_single_segment_solo__division_context_cascade_01():
    '''4/16 overrides 3/16.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_divisions([(4, 16)])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__division_context_cascade_02():
    '''4/16 overrides 3/16.
    Then 2/16 overrides 3/16.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_divisions([(4, 16)])
    red_segment.set_divisions([(2, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__division_context_cascade_03():
    '''4/16 overrides 3/16.
    Then 2/16 overrides 3/16.
    Then 5/16 overrides 2/16.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_divisions([(4, 16)])
    red_segment.set_divisions([(2, 16)], contexts=['Voice 1'])
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__division_context_cascade_04():
    '''Context order supersedes lexical order.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(2, 16)], contexts=['Voice 1'])
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_divisions([(4, 16)])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)