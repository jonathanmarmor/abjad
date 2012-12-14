from abjad.tools import durationtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
from experimental.symbolictimetools.Selector import Selector


class BackgroundMeasureSelector(Selector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select all measures that start during score::

        >>> score_specification.select_background_measures()
        BackgroundMeasureSelector(score_specification=ScoreSpecification(SegmentSpecificationInventory([SegmentSpecification('red')])))

    Select measures that start during score from ``3`` forward::

        >>> score_specification.select_background_measures(start=3)
        BackgroundMeasureSelector(score_specification=ScoreSpecification(SegmentSpecificationInventory([SegmentSpecification('red')])), start_identifier=3)

    Select measures that start during score up to but not including ``6``::

        >>> score_specification.select_background_measures(stop=6)
        BackgroundMeasureSelector(score_specification=ScoreSpecification(SegmentSpecificationInventory([SegmentSpecification('red')])), stop_identifier=6)

    Select measures from ``3`` up to but not including ``6``::

        >>> score_specification.select_background_measures(start=3, stop=6)
        BackgroundMeasureSelector(score_specification=ScoreSpecification(SegmentSpecificationInventory([SegmentSpecification('red')])), start_identifier=3, stop_identifier=6)

    Select all measures starting during segment ``'red'``::

        >>> red_segment.select_background_measures()
        BackgroundMeasureSelector(score_specification=ScoreSpecification(SegmentSpecificationInventory([SegmentSpecification('red')])), anchor='red')

    Select the last two measures during segment ``'red'``::

        >>> measures = red_segment.select_background_measures(start=-2)

    ::
    
        >>> z(measures)
        symbolictimetools.BackgroundMeasureSelector(
            score_specification=specificationtools.ScoreSpecification(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=4
                    )
                ),
            anchor='red',
            start_identifier=-2
            )

    Select all the measures that start during the three contiguous segments 
    starting with ``'red'``::

        >>> segments = score_specification.select_segments('red', ('red', 3))
        >>> measures = segments.select_background_measures()

    ::

        >>> z(measures)
        symbolictimetools.BackgroundMeasureSelector(
            anchor=symbolictimetools.SegmentSelector(
                start_identifier='red',
                stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3")
                )
            )

    Select the last two measures that start during the three contiguous segments 
    starting with ``'red'``::

        >>> measures = segments.select_background_measures(start=-2)

    ::

        >>> z(measures)
        symbolictimetools.BackgroundMeasureSelector(
            anchor=symbolictimetools.SegmentSelector(
                start_identifier='red',
                stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3")
                ),
            start_identifier=-2
            )

    Background measure symbolic timespans are immutable.
    '''

    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        result = type(self)(
            anchor=self.anchor, 
            start_identifier=self.start_identifier, stop_identifier=self.stop_identifier,
            time_relation=self.time_relation,
            timespan_modifications=self.timespan_modifications,
            selector_modifications=self.selector_modifications)
        result._score_specification = self.score_specification
        return result

    ### PRIVATE METHODS ###

    def _get_offsets(self, score_specification, context_name):
        r'''Evaluate start and stop offsets when selector is applied
        to `score_specification`.

        Ignore `context_name`. 

        First slice according to self.start, self.stop if set.
        Then apply any modifications in selector modifications stack.

        Return pair.
        '''
        segment_specification = score_specification.get_start_segment_specification(self.anchor)
        segment_name = segment_specification.segment_name
        start, stop = self.identifiers
        start = start or 0
        stop = stop or None
        time_signatures = segment_specification.time_signatures[start:stop]
        durations = [durationtools.Duration(x) for x in segment_specification.time_signatures]     
        durations_before = durations[:start]
        duration_before = sum(durations_before)
        start_offset = durationtools.Offset(duration_before)
        start_offset = score_specification.segment_offset_to_score_offset(segment_name, start_offset)
        time_signatures, start_offset = self._apply_selector_modifications(time_signatures, start_offset)
        durations = [durationtools.Duration(x) for x in time_signatures]
        duration = sum(durations)
        stop_offset = start_offset + duration
        start_offset, stop_offset = self._apply_timespan_modifications(start_offset, stop_offset)
        return start_offset, stop_offset
