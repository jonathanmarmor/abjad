# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_InstrumentationSpecifier___eq___01():

    instrumentation_1 = instrumenttools.InstrumentationSpecifier()
    performer_1 = instrumenttools.Performer('Flute')
    performer_1.instruments.append(instrumenttools.Flute())
    instrumentation_1.performers.append(performer_1)
    performer_2 = instrumenttools.Performer('Guitar')
    performer_2.instruments.append(instrumenttools.Guitar())
    instrumentation_1.performers.append(performer_2)

    instrumentation_2 = instrumenttools.InstrumentationSpecifier()
    performer_3 = instrumenttools.Performer('Flute')
    performer_3.instruments.append(instrumenttools.Flute())
    instrumentation_2.performers.append(performer_3)
    performer_4 = instrumenttools.Performer('Guitar')
    performer_4.instruments.append(instrumenttools.Guitar())
    instrumentation_2.performers.append(performer_4)

    instrumentation_3 = instrumenttools.InstrumentationSpecifier()
    performer_5 = instrumenttools.Performer('Violin')
    performer_5.instruments.append(instrumenttools.Violin())
    instrumentation_3.performers.append(performer_5)
    performer_6 = instrumenttools.Performer('Cello')
    performer_6.instruments.append(instrumenttools.Cello())
    instrumentation_3.performers.append(performer_6)

    assert     instrumentation_1 == instrumentation_2
    assert     instrumentation_2 == instrumentation_1
    assert not instrumentation_1 != instrumentation_2
    assert not instrumentation_2 != instrumentation_1

    assert not instrumentation_1 == instrumentation_3
    assert not instrumentation_3 == instrumentation_1
    assert     instrumentation_1 != instrumentation_3
    assert     instrumentation_3 != instrumentation_1

    assert not instrumentation_2 == instrumentation_3
    assert not instrumentation_3 == instrumentation_2
    assert     instrumentation_2 != instrumentation_3
    assert     instrumentation_3 != instrumentation_2