from abjad import *


def test_Component_select_vertical_moment_01():

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

    def piano_staff_moment(expr):
        return expr.select_vertical_moment(governor=piano_staff)

    vm = piano_staff_moment(piano_staff[1][0])
    assert vm.leaves == (piano_staff[0][0], piano_staff[1][0])

    vm = piano_staff_moment(piano_staff[1][1])
    assert vm.leaves == (piano_staff[0][0], piano_staff[1][1])

    vm = piano_staff_moment(piano_staff[1][2])
    assert vm.leaves == (piano_staff[0][1], piano_staff[1][2])

    vm = piano_staff_moment(piano_staff[1][3])
    assert vm.leaves == (piano_staff[0][1], piano_staff[1][3])


def test_Component_select_vertical_moment_02():

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

    vm = piano_staff[1][0].select_vertical_moment()
    assert vm.leaves == (score[0][0][0], piano_staff[0][0], piano_staff[1][0])

    vm = piano_staff[1][1].select_vertical_moment()
    assert vm.leaves == (score[0][0][0], piano_staff[0][0], piano_staff[1][1])

    vm = piano_staff[1][2].select_vertical_moment()
    assert vm.leaves == (score[0][0][1], piano_staff[0][1], piano_staff[1][2])

    vm = piano_staff[1][3].select_vertical_moment()
    assert vm.leaves == (score[0][0][2], piano_staff[0][1], piano_staff[1][3])