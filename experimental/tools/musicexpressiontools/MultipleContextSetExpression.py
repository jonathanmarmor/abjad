# -*- encoding: utf-8 -*-
import copy
from experimental.tools.musicexpressiontools.TimeContiguousAnchoredSetExpression \
    import TimeContiguousAnchoredSetExpression


class MultipleContextSetExpression(TimeContiguousAnchoredSetExpression):
    r'''Multiple-context set expression.

    Set `attribute` to `source_expression` for `target_timespan` over
    all `contexts`:

    ::

        >>> score_template = \
        ...     templatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=4)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> multiple_context_set_expression = \
        ...     red_segment.set_time_signatures([(4, 8), (3, 8)])

    ::

        >>> print format(multiple_context_set_expression)
        musicexpressiontools.MultipleContextSetExpression(
            attribute='time_signatures',
            source_expression=musicexpressiontools.IterablePayloadExpression(
                payload=(
                    (4, 8),
                    (3, 8),
                    ),
                ),
            target_timespan='red',
            persist=True,
            )

    Set methods create multiple-context set expressions.
    '''

    ### INITIAILIZER ###

    def __init__(
            self,
            attribute=None,
            source_expression=None,
            target_timespan=None,
            scope_names=None,
            persist=True,
            truncate=None,
            ):
        TimeContiguousAnchoredSetExpression.__init__(
            self,
            attribute=attribute,
            source_expression=source_expression,
            target_timespan=target_timespan,
            persist=persist,
            truncate=truncate,
            )
        assert isinstance(scope_names, (list, type(None)))
        self._scope_names = scope_names

    ### PRIVATE METHODS ###

    def _attribute_to_single_context_set_expression_class(self, attribute):
        from experimental.tools import musicexpressiontools
        return {
            'time_signatures': musicexpressiontools.SingleContextTimeSignatureSetExpression,
            'divisions': musicexpressiontools.SingleContextDivisionSetExpression,
            'rhythm': musicexpressiontools.SingleContextRhythmSetExpression,
            }[attribute]

    ### PUBLIC PROPERTIES ###

    @property
    def scope_names(self):
        r'''Multiple-context set expression target context names.

        Returns list or none.
        '''
        return self._scope_names

    ### PUBLIC METHODS ###

    def evaluate(self):
        r'''Evaluate multiple-context set expression.

        Returns list of single-context set expressions.
        '''
        single_context_set_expressions = []
        single_context_set_expression_class = \
            self._attribute_to_single_context_set_expression_class(
                self.attribute)
        if self.scope_names is None:
            scope_names = [None]
        else:
            scope_names = self.scope_names
        for scope_name in scope_names:
            target_timespan = copy.deepcopy(self.target_timespan)
            single_context_set_expression = \
                single_context_set_expression_class(
                    source_expression=self.source_expression,
                    target_timespan=target_timespan,
                    scope_name=scope_name,
                    persist=self.persist,
                    )
            single_context_set_expression._score_specification = \
                self.score_specification
            single_context_set_expression._lexical_rank = \
                self._lexical_rank
            single_context_set_expressions.append(
                single_context_set_expression)
        if self.attribute == 'divisions':
            for single_context_set_expression in \
                single_context_set_expressions:
                single_context_set_expression._truncate = self.truncate
        return single_context_set_expressions

    def evaluate_and_store_in_root_specification(self):
        r'''Evaluate multiple-context set expression
        and store in root specification.

        Returns none.
        '''
        fresh_single_context_set_expressions = self.evaluate()
        assert all(x.fresh for x in fresh_single_context_set_expressions)
        self.root_specification.fresh_single_context_set_expressions.extend(
            fresh_single_context_set_expressions)
