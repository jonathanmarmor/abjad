from abjad import *


def test_VerticalMoment___eq___01():

    score = Score([])
    score.append(Staff([tuplettools.FixedDurationTuplet(Duration(4, 8), notetools.make_repeated_notes(3))]))
    piano_staff = scoretools.PianoStaff([])
    piano_staff.append(Staff(notetools.make_repeated_notes(2, Duration(1, 4))))
    piano_staff.append(Staff(notetools.make_repeated_notes(4)))
    contexttools.ClefMark('bass')(piano_staff[1])
    score.append(piano_staff)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(list(reversed(score.select_leaves())))

    r'''
    \new Score <<
        \new Staff {
            \times 4/3 {
                d''8
                c''8
                b'8
            }
        }
        \new PianoStaff <<
            \new Staff {
                a'4
                g'4
            }
            \new Staff {
                \clef "bass"
                f'8
                e'8
                d'8
                c'8
            }
        >>
    >>
    '''

    vertical_moment_1 = piano_staff.select_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"

    vertical_moment_2 = piano_staff.select_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"

    assert vertical_moment_1 == vertical_moment_2
    assert not vertical_moment_1 != vertical_moment_2


def test_VerticalMoment___eq___02():

    score = Score([])
    score.append(Staff([tuplettools.FixedDurationTuplet(Duration(4, 8), notetools.make_repeated_notes(3))]))
    piano_staff = scoretools.PianoStaff([])
    piano_staff.append(Staff(notetools.make_repeated_notes(2, Duration(1, 4))))
    piano_staff.append(Staff(notetools.make_repeated_notes(4)))
    contexttools.ClefMark('bass')(piano_staff[1])
    score.append(piano_staff)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(list(reversed(score.select_leaves())))

    r'''
    \new Score <<
        \new Staff {
            \times 4/3 {
                d''8
                c''8
                b'8
            }
        }
        \new PianoStaff <<
            \new Staff {
                a'4
                g'4
            }
            \new Staff {
                \clef "bass"
                f'8
                e'8
                d'8
                c'8
            }
        >>
    >>
    '''

    vertical_moment_1 = piano_staff.select_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"

    vertical_moment_2 = piano_staff[:2].select_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(Staff{2}, a'4, Staff{4}, e'8)"

    assert not vertical_moment_1 == vertical_moment_2
    assert vertical_moment_1 != vertical_moment_2