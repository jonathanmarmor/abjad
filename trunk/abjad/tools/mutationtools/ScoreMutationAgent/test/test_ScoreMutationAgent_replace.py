# -*- encoding: utf-8 -*-
from abjad import *


def test_ScoreMutationAgent_replace_01():
    r'''Move parentage and spanners from two old notes to five new notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(staff[:2])
    b2 = spannertools.BeamSpanner(staff[2:])
    crescendo = spannertools.CrescendoSpanner(staff[:])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ \<
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        )

    old_notes = staff[1:3]
    new_notes = 5 * Note(12, (1, 16))
    mutate(old_notes).replace(new_notes)

    "Equivalent to staff[1:3] = new_notes"

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ ] \<
            c''16
            c''16
            c''16
            c''16
            c''16
            f'8 [ ] \!
        }
        '''
        )


def test_ScoreMutationAgent_replace_02():
    r'''Move parentage and spanners from one old note to five new notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(staff[:2])
    b2 = spannertools.BeamSpanner(staff[2:])
    crescendo = spannertools.CrescendoSpanner(staff[:])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ \<
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        )

    new_notes = 5 * Note(12, (1, 16))
    mutate(staff[:1]).replace(new_notes)
    #staff[:1] = new_notes

    "Equivalent to staff[:1] = new_notes."

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c''16 [ \<
            c''16
            c''16
            c''16
            c''16
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        )


def test_ScoreMutationAgent_replace_03():
    r'''Move parentage and spanners from two old notes to five new notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(staff[:2])
    b2 = spannertools.BeamSpanner(staff[2:])
    crescendo = spannertools.CrescendoSpanner(staff[:])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ \<
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        )

    new_notes = 5 * Note(12, (1, 16))
    mutate(staff[:2]).replace(new_notes)
    #staff[:2] = new_notes

    "Equivalent to staff[:2] = new_notes."

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c''16 [ \<
            c''16
            c''16
            c''16
            c''16 ]
            e'8 [
            f'8 ] \!
        }
        '''
        )


def test_ScoreMutationAgent_replace_04():
    r'''Move parentage and spanners from three old notes to five new notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(staff[:2])
    b2 = spannertools.BeamSpanner(staff[2:])
    crescendo = spannertools.CrescendoSpanner(staff[:])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ \<
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        )

    new_notes = 5 * Note(12, (1, 16))
    mutate(staff[:3]).replace(new_notes)
    #staff[:3] = new_notes

    "Equivalent to staff[:3] = new_notes."

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c''16 \<
            c''16
            c''16
            c''16
            c''16
            f'8 [ ] \!
        }
        '''
        )


def test_ScoreMutationAgent_replace_05():
    r'''Move parentage and spanners from four old notes to five new notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(staff[:2])
    b2 = spannertools.BeamSpanner(staff[2:])
    crescendo = spannertools.CrescendoSpanner(staff[:])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ \<
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        )

    new_notes = 5 * Note(12, (1, 16))
    mutate(staff[:]).replace(new_notes)
    #staff[:] = new_notes

    "Equivalent to staff[:] = new_notes."

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c''16 \<
            c''16
            c''16
            c''16
            c''16 \!
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_ScoreMutationAgent_replace_06():
    r'''Move parentage and spanners from container to children of container.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(staff[0][:])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \new Voice {
                c'8 [
                d'8
                e'8
                f'8 ]
            }
        }
        '''
        )

    voice_selection = staff[:1]
    voice = voice_selection[0]
    old_components = mutate(voice_selection).replace(staff[0][:])

    "Equivalent to staff[:1] = staff[0][:]."

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(voice) == 0