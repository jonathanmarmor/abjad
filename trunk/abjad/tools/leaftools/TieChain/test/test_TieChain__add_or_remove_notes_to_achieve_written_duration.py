from abjad import *


def test_TieChain__add_or_remove_notes_to_achieve_written_duration_01():
    '''Change trivial tie chain to nontrivial tie chain.
    '''

    staff = Staff("c'8 [ ]")
    tie_chain = staff[0].select_tie_chain()
    tie_chain._add_or_remove_notes_to_achieve_written_duration(Duration(5, 32))

    r'''
    \new Staff {
        c'8 [ ~
        c'32 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [ ~\n\tc'32 ]\n}"


def test_TieChain__add_or_remove_notes_to_achieve_written_duration_02():
    '''Change nontrivial tie chain to trivial tie chain.
    '''

    staff = Staff("c'8 [ ~ c'32 ]")
    tie_chain = staff[0].select_tie_chain()
    tie_chain._add_or_remove_notes_to_achieve_written_duration(Duration(1, 8))

    r'''
    \new Staff {
        c'8 [ ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [ ]\n}"