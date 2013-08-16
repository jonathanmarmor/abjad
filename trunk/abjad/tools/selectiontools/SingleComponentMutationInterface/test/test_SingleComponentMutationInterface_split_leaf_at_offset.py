# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_SingleComponentMutationInterface_split_leaf_at_offset_01():
    r'''Split note into assignable notes.
    Don't fracture spanners. Don't tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    halves = mutate(staff.select_leaves()[1]).split_leaf_at_offset(
        (1, 32), 
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'32
            d'16.
            e'8 ]
        }
        '''
        )


def test_SingleComponentMutationInterface_split_leaf_at_offset_02():
    r'''Split note into assignable notes.
    Fracture spanners. But don't tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    halves = mutate(staff.select_leaves()[1]).split_leaf_at_offset(
        (1, 32),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'32 ]
            d'16. [
            e'8 ]
        }
        '''
        )

    assert select(staff).is_well_formed()


def test_SingleComponentMutationInterface_split_leaf_at_offset_03():
    r'''Split note into assignable notes.
    Don't fracture spanners. But do tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    halves = mutate(staff.select_leaves()[1]).split_leaf_at_offset(
        (1, 32), 
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'32 ~
            d'16.
            e'8 ]
        }
        '''
        )

    assert select(staff).is_well_formed()


def test_SingleComponentMutationInterface_split_leaf_at_offset_04():
    r'''Split note into assignable notes.
    Fracture spanners and tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    halves = mutate(staff.select_leaves()[1]).split_leaf_at_offset(
        (1, 32), 
        fracture_spanners=True, 
        tie_split_notes=True,
        )

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'32 ] ~
            d'16. [
            e'8 ]
        }
        '''
        )


def test_SingleComponentMutationInterface_split_leaf_at_offset_05():
    r'''Split note into tuplet monads.
    Don't fracture spanners. Don't tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    halves = mutate(staff.select_leaves()[1]).split_leaf_at_offset(
        (1, 24), 
        tie_split_notes=False,
        )

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            \times 2/3 {
                d'16
            }
            \times 2/3 {
                d'8
            }
            e'8 ]
        }
        '''
        )

    assert select(staff).is_well_formed()


def test_SingleComponentMutationInterface_split_leaf_at_offset_06():
    r'''Notehead-assignable duration produces two notes.
    This test comes from a container-crossing spanner bug.
    '''

    voice = Voice(
        notetools.make_repeated_notes(1) + 
        [tuplettools.FixedDurationTuplet(
            Duration(2, 8), notetools.make_repeated_notes(3))])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        voice)
    spannertools.BeamSpanner(voice.select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            \times 2/3 {
                d'8
                e'8
                f'8 ]
            }
        }
        '''
        )

    halves = mutate(voice.select_leaves()[1]).split_leaf_at_offset(
        Duration(1, 24), 
        tie_split_notes=False,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            \times 2/3 {
                d'16
                d'16
                e'8
                f'8 ]
            }
        }
        '''
        )

    assert select(voice).is_well_formed()


def test_SingleComponentMutationInterface_split_leaf_at_offset_07():
    r'''Split duration equal to zero produces no change.
    '''

    note = Note("c'4")

    halves = mutate(note).split_leaf_at_offset(Duration(0))
    left, right = halves

    assert len(halves) == 2
    assert len(left) == 0
    assert len(right) == 1
    assert isinstance(right[0], Note)
    assert right[0].written_duration == Duration(1, 4)


def test_SingleComponentMutationInterface_split_leaf_at_offset_08():
    r'''Leaf duration less than split duration produces no change.
    '''

    note = Note("c'4")

    halves = mutate(note).split_leaf_at_offset(Duration(3, 4))
    left, right = halves

    assert len(halves) == 2
    assert len(left) == 1
    assert isinstance(left[0], Note)
    assert left[0].written_duration == Duration(1, 4)
    assert len(right) == 0


def test_SingleComponentMutationInterface_split_leaf_at_offset_09():
    r'''Split returns two lists of zero or more leaves.
    '''

    note = Note("c'4")
    halves = mutate(note).split_leaf_at_offset(
        Duration(1, 8), 
        tie_split_notes=False,
        )

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    assert halves[0][0] is note
    assert halves[1][0] is not note
    assert isinstance(halves[0][0], Note)
    assert isinstance(halves[1][0], Note)
    assert halves[0][0].written_duration == Duration(1, 8)
    assert halves[1][0].written_duration == Duration(1, 8)
    assert len(more(halves[0][0]).select_tie_chain()) == 1
    assert len(more(halves[1][0]).select_tie_chain()) == 1


def test_SingleComponentMutationInterface_split_leaf_at_offset_10():
    r'''Split returns two lists of zero or more.
    '''

    note = Note("c'4")
    halves = mutate(note).split_leaf_at_offset(Duration(1, 16))

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    assert isinstance(halves[0][0], Note)
    assert isinstance(halves[1][0], Note)
    assert halves[0][0].written_duration == Duration(1, 16)
    assert halves[1][0].written_duration == Duration(3, 16)


def test_SingleComponentMutationInterface_split_leaf_at_offset_11():
    r'''Nonassignable split duration with power-of-two denominator
    produces two lists.
    Left list contains two notes tied together.
    Right list contains only one note.
    '''

    note = Note("c'4")
    halves = mutate(note).split_leaf_at_offset(
        Duration(5, 32), 
        tie_split_notes=False,
        )

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 2
    assert len(halves[1]) == 1
    assert isinstance(halves[0][0], Note)
    assert isinstance(halves[0][1], Note)
    assert isinstance(halves[1][0], Note)
    assert halves[0][0].written_duration == Duration(4, 32)
    assert halves[0][1].written_duration == Duration(1, 32)
    assert halves[1][0].written_duration == Duration(3, 32)
    assert len(more(halves[0][0]).select_tie_chain()) == 2
    assert len(more(halves[0][1]).select_tie_chain()) == 2
    assert len(more(halves[1][0]).select_tie_chain()) == 1


def test_SingleComponentMutationInterface_split_leaf_at_offset_12():
    r'''Lone spanned Leaf results in two spanned leaves.
    '''

    staff = Staff([Note("c'4")])
    tie = spannertools.TieSpanner(staff.select_leaves())
    halves = mutate(staff[0]).split_leaf_at_offset(Duration(1, 8))

    assert len(staff) == 2
    for leaf in staff.select_leaves():
        assert more(leaf).get_spanners() == set([tie])
        assert spannertools.get_the_only_spanner_attached_to_component(
            leaf, spannertools.TieSpanner) is tie
    assert select(staff).is_well_formed()


def test_SingleComponentMutationInterface_split_leaf_at_offset_13():
    r'''Spanners are unaffected by leaf split.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    b = spannertools.BeamSpanner(staff.select_leaves())

    halves = mutate(staff[0]).split_leaf_at_offset(
        Duration(1, 16), 
        tie_split_notes=False,
        )

    assert len(staff) == 5
    for l in staff.select_leaves():
        assert more(l).get_spanners() == set([b])
        assert l._get_spanner(spannertools.BeamSpanner) is b
    assert select(staff).is_well_formed()


def test_SingleComponentMutationInterface_split_leaf_at_offset_14():
    r'''Split returns three leaves, two are tied.
    Spanner is shared by all 3 leaves.
    '''

    staff = Staff([Note("c'4")])
    tie = spannertools.TieSpanner(staff.select_leaves())
    halves = mutate(staff[0]).split_leaf_at_offset(Duration(5, 32))

    assert len(halves) == 2
    assert len(halves[0]) == 2
    assert len(halves[1]) == 1
    for l in staff.select_leaves():
        assert more(l).get_spanners() == set([tie])
        assert spannertools.get_the_only_spanner_attached_to_component(
            l, spannertools.TieSpanner) is tie
    assert select(staff).is_well_formed()


def test_SingleComponentMutationInterface_split_leaf_at_offset_15():
    r'''Split leaf is not tied again when a container containing it 
    is already tie-spanned.
    '''

    container = Container(notetools.make_repeated_notes(4))
    tie = spannertools.TieSpanner(container)
    halves = mutate(container[0]).split_leaf_at_offset(Duration(5, 64))

    assert spannertools.get_the_only_spanner_attached_to_component(container,
    spannertools.TieSpanner) is tie
    assert tie.components == (container, )
    for l in container.select_leaves():
        assert not more(l).get_spanners()
    assert select(container).is_well_formed()


def test_SingleComponentMutationInterface_split_leaf_at_offset_16():
    r'''Split leaf is not tied again when a container containing it 
    is already tie-spanned.
    '''

    staff = Staff(Container(notetools.make_repeated_notes(4)) * 2)
    tie = spannertools.TieSpanner(staff[:])
    halves = mutate(staff[0][0]).split_leaf_at_offset(Duration(5, 64))

    assert tie.components == tuple(staff[:])
    for v in staff:
        assert more(v).get_spanners() == set([tie])
        for l in v.select_leaves():
            assert not more(l).get_spanners()
            assert l._parent is v
    assert select(staff).is_well_formed()


def test_SingleComponentMutationInterface_split_leaf_at_offset_17():
    r'''After grace notes are removed from first leaf in bipartition.
    '''

    note = Note("c'4")
    leaftools.GraceContainer([Note(0, (1, 32))], kind = 'after')(note)
    halves = mutate(note).split_leaf_at_offset(Duration(1, 8))

    assert not hasattr(halves[0][0], 'after_grace')
    assert len(halves[1][0].after_grace) == 1


def test_SingleComponentMutationInterface_split_leaf_at_offset_18():
    r'''After grace notes are removed from first tied leaves in bipartition.
    '''

    note = Note("c'4")
    leaftools.GraceContainer([Note(0, (1, 32))], kind = 'after')(note)
    halves = mutate(note).split_leaf_at_offset(Duration(5, 32))

    assert len(halves) == 2
    assert not hasattr(halves[0][0], 'after_grace')
    assert not hasattr(halves[0][1], 'after_grace')
    assert len(halves[1]) == 1
    assert len(halves[1][0].after_grace) == 1


def test_SingleComponentMutationInterface_split_leaf_at_offset_19():
    r'''Grace notes are removed from second leaf in bipartition.
    '''

    note = Note("c'4")
    leaftools.GraceContainer([Note(0, (1, 32))])(note)
    halves = mutate(note).split_leaf_at_offset(Duration(1, 16))

    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    assert len(halves[0][0].grace) == 1
    assert not hasattr(halves[1][0], 'grace')