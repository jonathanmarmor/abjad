from abjad import *


def test_Scale_make_score_01():

    scale = tonalanalysistools.Scale('E', 'major')
    score = scale.make_score()

    r'''
    \new Score \with {
        tempoWholesPerMinute = #(ly:make-moment 30 1)
    } <<
        \new Staff {
            \key e \major
            e'8
            fs'8
            gs'8
            a'8
            b'8
            cs''8
            ds''8
            e''8
            ds''8
            cs''8
            b'8
            a'8
            gs'8
            fs'8
            e'4
        }
    >>
    '''

    assert score.lilypond_format == "\\new Score \\with {\n\ttempoWholesPerMinute = #(ly:make-moment 30 1)\n} <<\n\t\\new Staff {\n\t\t\\key e \\major\n\t\te'8\n\t\tfs'8\n\t\tgs'8\n\t\ta'8\n\t\tb'8\n\t\tcs''8\n\t\tds''8\n\t\te''8\n\t\tds''8\n\t\tcs''8\n\t\tb'8\n\t\ta'8\n\t\tgs'8\n\t\tfs'8\n\t\te'4\n\t}\n>>"