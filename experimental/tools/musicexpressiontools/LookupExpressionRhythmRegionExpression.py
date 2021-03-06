# -*- encoding: utf-8 -*-
import copy
from abjad.tools import timespantools
from abjad.tools import timespantools
from experimental.tools.musicexpressiontools.RhythmRegionExpression \
    import RhythmRegionExpression


class LookupExpressionRhythmRegionExpression(RhythmRegionExpression):
    r'''Lookup expression rhythm region expression.
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        source_expression=None, 
        division_list=None,
        region_start_offset=None, 
        start_offset=None, 
        total_duration=None, 
        voice_name=None,
        ):
        RhythmRegionExpression.__init__(
            self, 
            source_expression=source_expression,
            start_offset=start_offset, 
            total_duration=total_duration, 
            voice_name=voice_name,
            )
        self._division_list = division_list
        self._region_start_offset = region_start_offset

    ### PRIVATE METHODS ###

    def evaluate(self):
        r'''Evaluate lookup expression rhythm region expression.

        Returns none when nonevaluable.

        Returns start-positioned rhythm payload expression when evaluable.
        '''
        from experimental.tools import musicexpressiontools
        expression = self.source_expression.evaluate()
        if expression is None:
            return
        if isinstance(expression, musicexpressiontools.RhythmMakerExpression):
            rhythm_maker = expression.payload
            region_expression = \
                musicexpressiontools.RhythmMakerRhythmRegionExpression(
                rhythm_maker,
                self.division_list,
                self.start_offset,
                self.voice_name,
                )
            result = region_expression.evaluate()
        elif isinstance(
            expression,
            musicexpressiontools.StartPositionedRhythmPayloadExpression):
            wrapped_component = copy.deepcopy(expression.payload)
            region_expression = \
                musicexpressiontools.LiteralRhythmRegionExpression(
                wrapped_component,
                self.start_offset,
                self.total_duration,
                self.voice_name,
                )
            result = region_expression.evaluate()
        else:
            raise TypeError(expression)
        assert isinstance(
            result,
            musicexpressiontools.StartPositionedRhythmPayloadExpression)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def division_list(self):
        r'''Lookup expression rhythm region expression division list.

        Returns division list.
        '''
        return self._division_list

    @property
    def region_start_offset(self):
        r'''Lookup expression rhythm region expression region start offset.

        Returns offset.
        '''
        return self._region_start_offset
