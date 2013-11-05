# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRangeInventory_storage_format_01():

    inventory = pitchtools.PitchRangeInventory(['[A0, C8]', '[C4, D5]'])

    assert testtools.compare(
        inventory.storage_format,
        r'''
        pitchtools.PitchRangeInventory([
            pitchtools.PitchRange(
                '[A0, C8]'
                ),
            pitchtools.PitchRange(
                '[C4, D5]'
                ),
            ])
        ''',
        )