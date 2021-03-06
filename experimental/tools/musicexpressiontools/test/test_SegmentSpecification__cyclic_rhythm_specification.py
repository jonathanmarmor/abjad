# -*- encoding: utf-8 -*-
import pytest
from experimental import *


def test_SegmentSpecification__cyclic_rhythm_specification_01():

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_rhythm = red_segment.select_leaves('Voice 1')
    blue_rhythm = blue_segment.select_leaves('Voice 1')
    red_segment.set_rhythm(blue_rhythm)

    assert pytest.raises(Exception, 'score_specification.interpret()')
