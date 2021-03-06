# -*- encoding: utf-8 -*-
from experimental import *


def test_ScoreSpecification__interpret_01():
    r'''Empty score specification interprets.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)

    score = score_specification.interpret()

    assert systemtools.TestManager.compare(
        score,
        r'''
        \context Score = "Grouped Rhythmic Staves Score" <<
            \context TimeSignatureContext = "TimeSignatureContext" {
            }
            \context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
                \context RhythmicStaff = "Staff 1" {
                    \context Voice = "Voice 1" {
                    }
                }
            >>
        >>
        '''
        )

    # TODO: remove me after compare works above
    assert format(score) == '\\context Score = "Grouped Rhythmic Staves Score" <<\n\t\\context TimeSignatureContext = "TimeSignatureContext" {\n\t}\n\t\\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<\n\t\t\\context RhythmicStaff = "Staff 1" {\n\t\t\t\\context Voice = "Voice 1" {\n\t\t\t}\n\t\t}\n\t>>\n>>'


def test_ScoreSpecification__interpret_02():
    r'''Empty score specification with empty segment specification interprets.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification_1 = musicexpressiontools.ScoreSpecification(score_template)

    score_1 = score_specification_1.interpret()

    score_specification_2 = musicexpressiontools.ScoreSpecification(score_template)
    red_segment = score_specification_2.append_segment(name='red')
    score_2 = score_specification_2.interpret()

    assert format(score_1) == format(score_2)


def test_ScoreSpecification__interpret_03():
    r'''Time signatures only.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])

    score = score_specification.interpret()

    assert systemtools.TestManager.compare(
        score,
        r'''
        \context Score = "Grouped Rhythmic Staves Score" <<
            \context TimeSignatureContext = "TimeSignatureContext" {
                {
                    \time 4/8
                    s1 * 1/2
                }
                {
                    \time 3/8
                    s1 * 3/8
                }
            }
            \context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
                \context RhythmicStaff = "Staff 1" {
                    \context Voice = "Voice 1" {
                        {
                            s1 * 1/2
                        }
                        {
                            s1 * 3/8
                        }
                    }
                }
            >>
        >>
        '''
        )

    # TODO: remove after compare works above
    assert format(score) == '\\context Score = "Grouped Rhythmic Staves Score" <<\n\t\\context TimeSignatureContext = "TimeSignatureContext" {\n\t\t{\n\t\t\t\\time 4/8\n\t\t\ts1 * 1/2\n\t\t}\n\t\t{\n\t\t\t\\time 3/8\n\t\t\ts1 * 3/8\n\t\t}\n\t}\n\t\\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<\n\t\t\\context RhythmicStaff = "Staff 1" {\n\t\t\t\\context Voice = "Voice 1" {\n\t\t\t\t{\n\t\t\t\t\ts1 * 1/2\n\t\t\t\t}\n\t\t\t\t{\n\t\t\t\t\ts1 * 3/8\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t>>\n>>'
