import copy
from abjad.tools import contexttools
from abjad.tools import iotools
from abjad.tools import marktools
from abjad.tools import pitchtools
from abjad.tools import spannertools
from abjad.tools.abctools import AbjadObject


class SetMethodMixin(AbjadObject):
    '''Set method mixin.
    '''

    ### PRIVATE METHODS ###

    def _all_are_expressions(self, expr):
        from experimental.tools import specificationtools
        if isinstance(expr, (tuple, list)):
            if all([isinstance(x, specificationtools.Expression) for x in expr]):
                return True
        return False

    def _attribute_to_set_expression_class(self, attribute):
        from experimental.tools import specificationtools
        return {
            'aggregate': specificationtools.AggregateSetExpression,
            'articulation': specificationtools.ArticulationSetExpression,
            'dynamic': specificationtools.DynamicSetExpression,
            'dynamic_handler': specificationtools.DynamicHandlerSetExpression,
            'leaf_color': specificationtools.LeafColorSetExpression,
            'mark': specificationtools.MarkSetExpression,
            'markup': specificationtools.MarkupSetExpression,
            'reigster': specificationtools.RegisterSetExpression,
            'pitch': specificationtools.PitchSetExpression,
            'pitch_class_transform': specificationtools.PitchClassTransformSetExpression,
            'spanner': specificationtools.SpannerSetExpression,
            }[attribute]

    def _expr_to_expression(self, expr):
        from abjad.tools import rhythmmakertools
        from experimental.tools import specificationtools
        if isinstance(expr, specificationtools.Expression):
            return expr
        elif self._all_are_expressions(expr):
            return specificationtools.ExpressionInventory(expr)
        elif isinstance(expr, (tuple, list)):
            return specificationtools.IterablePayloadExpression(expr)
        elif isinstance(expr, (str)):
            component = iotools.p(expr)
            return specificationtools.StartPositionedRhythmPayloadExpression([component], start_offset=0)
        elif isinstance(expr, rhythmmakertools.RhythmMaker):
            return specificationtools.RhythmMakerExpression(expr)
        else:
            raise TypeError('do not know how to change {!r} to expression.'.format(expr))

    def _store_leaf_set_expression(self, attribute, source_expression):
        from experimental.tools import specificationtools
        set_expression_class = self._attribute_to_set_expression_class(attribute)
        source_expression = self._expr_to_expression(source_expression)
        if isinstance(self, specificationtools.SelectExpression):
            target_select_expression_inventory = specificationtools.SelectExpressionInventory([self])
        elif isinstance(self, specificationtools.SelectExpressionInventory):
            target_select_expression_inventory = self
        else:
            raise TypeError(self)
        leaf_set_expression = set_expression_class(
            source_expression=source_expression,
            target_select_expression_inventory=target_select_expression_inventory
            )
        assert self.score_specification is not None
        leaf_set_expression._score_specification = self.score_specification
        leaf_set_expression._lexical_rank = self.score_specification._next_lexical_rank
        self.score_specification._next_lexical_rank += 1
        self.score_specification.postrhythm_set_expressions.append(leaf_set_expression)
        return leaf_set_expression

    ### PUBLIC METHODS ###

    def set_aggregate(self, source_expression):
        r'''Set aggregate to `source_expression`.

        Return aggregate set expression.
        '''
        from experimental.tools import specificationtools
        assert isinstance(source_expression, list), repr(source_expression)
        source_expression = specificationtools.PayloadExpression(payload=source_expression)
        attribute = 'aggregate'
        return self._store_leaf_set_expression(attribute, source_expression)

    def set_articulation(self, source_expression):
        r'''Set articulation to `source_expression`.

        Return articulation set expression.
        '''
        from experimental.tools import specificationtools
        if isinstance(source_expression, marktools.Articulation):
            articulation_list = [source_expression]
        elif isinstance(source_expression, str):
            articulation = marktools.Articulation(source_expression)
            articulation_list = [articulation]
        elif isinstance(source_expression, list):
            articulation_list = [marktools.Articulation(x) for x in source_expression]
        source_expression = specificationtools.PayloadExpression(payload=articulation_list)
        attribute = 'articulation'
        return self._store_leaf_set_expression(attribute, source_expression)

    def set_dynamic(self, source_expression):
        r'''Set dynamic to `source_expression`.

        Return dynamic set expression.
        '''
        from experimental.tools import specificationtools
        dynamic_mark = contexttools.DynamicMark(source_expression)
        source_expression = specificationtools.PayloadExpression(payload=dynamic_mark)
        attribute = 'dynamic'
        return self._store_leaf_set_expression(attribute, source_expression)

    def set_leaf_color(self, source_expression):
        r'''Set leaf color to `source_expression`.

        Return leaf color set expression.
        '''
        from experimental.tools import specificationtools
        assert isinstance(source_expression, str), repr(source_expression)
        source_expression = specificationtools.PayloadExpression(payload=source_expression)
        attribute = 'leaf_color'
        return self._store_leaf_set_expression(attribute, source_expression)

    def set_mark(self, source_expression):
        r'''Set mark to `source_expression`.

        Return mark set expression.
        '''
        from experimental.tools import specificationtools
        assert isinstance(source_expression, marktools.Mark), repr(source_expression)
        source_expression = specificationtools.PayloadExpression(payload=source_expression)
        attribute = 'mark'
        return self._store_leaf_set_expression(attribute, source_expression)

    def set_markup(self, source_expression):
        r'''Set markup to `source_expression`.

        Return markup set expression.
        '''
        from experimental.tools import specificationtools
        source_expression = specificationtools.PayloadExpression(payload=source_expression)
        attribute = 'markup'
        return self._store_leaf_set_expression(attribute, source_expression)

    def set_pitch_class_transform(self, source_expression):
        r'''Set pitch class transform to `source_expression`.

        Return pitch-class transform set expression.
        '''
        from experimental.tools import specificationtools
        pitch_class_transform_expression = specificationtools.PitchClassTransformExpression(source_expression)
        source_expression = specificationtools.PayloadExpression(payload=pitch_class_transform_expression)
        attribute = 'pitch_class_transform'
        return self._store_leaf_set_expression(attribute, source_expression)

    def set_pitch(self, source_expression):
        r'''Set pitches to `source_expression`.

        Return pitch set expression.
        '''
        from experimental.tools import specificationtools
        assert isinstance(source_expression, specificationtools.StatalServerCursor), repr(source_expression)
        source_expression = specificationtools.StatalServerCursorExpression(source_expression)
        attribute = 'pitch'
        return self._store_leaf_set_expression(attribute, source_expression)

    def set_register(self, source_expression):
        r'''Set register to `source_expression`.

        Return register set expression.
        '''
        from experimental.tools import specificationtools
        assert isinstance(source_expression, pitchtools.OctaveTranspositionMapping), repr(source_expression)
        source_expression = specificationtools.PayloadExpression(payload=source_expression)
        attribute = 'reigster'
        return self._store_leaf_set_expression(attribute, source_expression)