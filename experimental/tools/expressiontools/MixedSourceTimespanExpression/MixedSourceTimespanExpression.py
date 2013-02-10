from abjad.tools import abctools
from experimental.tools.expressiontools.TimespanExpression import TimespanExpression


class MixedSourceTimespanExpression(TimespanExpression):
    r'''Mixed-source_expression timespan expression.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> blue_segment = score_specification.append_segment(name='blue')

    Mixed-source_expression timespan.

    Mixed-source_expression timespan starting at the left edge of the last measure
    that starts during segment ``'red'``
    and stoppding at the right edge of the first measure 
    that starts during segment ``'blue'``::

        >>> measure = red_segment.select_measures('Voice 1')[-1:]
        >>> start_offset = measure.start_offset

    ::

        >>> measure = blue_segment.select_measures('Voice 1')[:1]
        >>> stop_offset = measure.stop_offset
        
    ::

        >>> timespan = expressiontools.MixedSourceTimespanExpression(start_offset, stop_offset)

    ::

        >>> z(timespan)
        expressiontools.MixedSourceTimespanExpression(
            start_offset=expressiontools.OffsetExpression(
                anchor=expressiontools.MeasureSelectExpression(
                    anchor='red',
                    voice_name='Voice 1',
                    callbacks=expressiontools.CallbackInventory([
                        'result = self._getitem__(payload_expression, slice(-1, None, None))'
                        ])
                    )
                ),
            stop_offset=expressiontools.OffsetExpression(
                anchor=expressiontools.MeasureSelectExpression(
                    anchor='blue',
                    voice_name='Voice 1',
                    callbacks=expressiontools.CallbackInventory([
                        'result = self._getitem__(payload_expression, slice(None, 1, None))'
                        ])
                    ),
                edge=Right
                )
            )

    Mixed-source_expression timespan expression properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, start_offset=None, stop_offset=None, callbacks=None):
        from experimental.tools import specificationtools
        from experimental.tools import expressiontools
        assert isinstance(start_offset, (expressiontools.OffsetExpression, type(None))), repr(start_offset)
        assert isinstance(stop_offset, (expressiontools.OffsetExpression, type(None))), repr(stop_offset)
        TimespanExpression.__init__(self, callbacks=callbacks)
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### PRIVATE METHODS ###

    def evaluate(self):
        raise NotImplementedError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        '''Mixed-source_expression timespan start offset specified by user.

        Return offset or none.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        '''Mixed-source_expression timepsan stop offset specified by user.

        Return offset or none.
        '''
        return self._stop_offset
