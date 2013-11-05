# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Performer_instrument_count_01():

    performer = instrumenttools.Performer('Flutist')
    assert performer.instrument_count == 0

    performer.instruments.append(instrumenttools.Flute())
    assert performer.instrument_count == 1

    performer.instruments.append(instrumenttools.Piccolo())
    assert performer.instrument_count == 2