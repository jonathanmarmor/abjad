# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.SingleContextSetExpression \
    import SingleContextSetExpression


class SingleContextRhythmSetExpression(SingleContextSetExpression):
    r'''Single-context rhythm set expression.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        source_expression=None,
        target_timespan=None,
        scope_name=None,
        fresh=True,
        persist=True,
        ):
        SingleContextSetExpression.__init__(
            self,
            attribute='rhythm',
            source_expression=source_expression,
            target_timespan=target_timespan,
            scope_name=scope_name,
            fresh=fresh,
            persist=persist,
            )

    ### PUBLIC METHODS ###

    def evaluate(self):
        r'''Evaluate single-context rhythm set expression.

        Returns timespan-delimited single-context rhythm set expression.
        '''
        from experimental.tools import musicexpressiontools
        target_timespan = self._evaluate_anchor_timespan()
        expression = \
            musicexpressiontools.TimespanScopedSingleContextRhythmSetExpression(
            source_expression=self.source_expression,
            target_timespan=target_timespan,
            scope_name=self.scope_name,
            fresh=self.fresh,
            )
        expression._lexical_rank = self._lexical_rank
        return expression
