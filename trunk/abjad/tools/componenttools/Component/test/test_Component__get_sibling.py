from abjad import *


def test_Component__get_sibling_01():

    staff = Staff("c' d' e' f'")
    assert staff[1]._get_sibling(2) is staff[3]
    assert staff[1]._get_sibling(1) is staff[2]
    assert staff[1]._get_sibling(0) is staff[1]
    assert staff[1]._get_sibling(-1) is staff[0]


def test_Component__get_sibling_02():
    '''Return none when index is out of range.
    '''

    staff = Staff("c' d' e' f'")
    assert staff[1]._get_sibling(99) is None


def test_Component__get_sibling_03():
    '''Return none when component has no parent.
    '''

    staff = Staff("c' d' e' f'")
    assert staff._get_sibling(1) is None