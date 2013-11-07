# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import rhythmtreetools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject


class Meter(AbjadObject):
    '''A rhythm tree-based model of nested time signature groupings.

    The structure of the tree corresponds to the monotonically increasing
    sequence of factors of the time signature's numerator.

    Each deeper level of the tree divides the previous by the next 
    factor in sequence.

    Prime divisions greater than ``3`` are converted to sequences of 
    ``2`` and ``3`` summing to that prime. 
    Hence ``5`` becomes ``3+2`` and ``7`` becomes ``3+2+2``.

    The meter models many parts of the common practice 
    understanding of meter:

    ::

        >>> meter = timesignaturetools.Meter((4, 4))

    ::

        >>> meter
        Meter('(4/4 (1/4 1/4 1/4 1/4))')

    ::

        >>> print meter.pretty_rtm_format
        (4/4 (
            1/4
            1/4
            1/4
            1/4))

    ::

        >>> meter = timesignaturetools.Meter((3, 4))
        >>> print meter.pretty_rtm_format
        (3/4 (
            1/4
            1/4
            1/4))

    ::

        >>> meter = timesignaturetools.Meter((6, 8))
        >>> print meter.pretty_rtm_format
        (6/8 (
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))))

    ::

        >>> meter = timesignaturetools.Meter((5, 4))
        >>> print meter.pretty_rtm_format
        (5/4 (
            (3/4 (
                1/4
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

    ::

        >>> meter = timesignaturetools.Meter(
        ...     (5, 4), decrease_durations_monotonically=False)
        >>> print meter.pretty_rtm_format
        (5/4 (
            (2/4 (
                1/4
                1/4))
            (3/4 (
                1/4
                1/4
                1/4))))

    ::

        >>> meter = timesignaturetools.Meter((12, 8))
        >>> print meter.pretty_rtm_format
        (12/8 (
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))))

    Returns meter object.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_decrease_durations_monotonically',
        '_denominator',
        '_numerator',
        '_root_node',
        )

    ### INITIALIZER ###

    def __init__(self, arg, decrease_durations_monotonically=True):

        def recurse(
            node, factors, denominator, decrease_durations_monotonically):
            if factors:
                factor, factors = factors[0], factors[1:]
                preprolated_duration = node.preprolated_duration / factor
                if factor in (2, 3, 4):
                    if factors:
                        for _ in range(factor):
                            child = rhythmtreetools.RhythmTreeContainer(
                                preprolated_duration=preprolated_duration)
                            node.append(child)
                            recurse(
                                child,
                                factors,
                                denominator,
                                decrease_durations_monotonically,
                                )
                    else:
                        for _ in range(factor):
                            node.append(
                                rhythmtreetools.RhythmTreeLeaf(
                                    preprolated_duration=(1, denominator)))
                else:
                    parts = [3]
                    total = 3
                    while total < factor:
                        if decrease_durations_monotonically:
                            parts.append(2)
                        else:
                            parts.insert(0, 2)
                        total += 2
                    for part in parts:
                        grouping = rhythmtreetools.RhythmTreeContainer(
                            preprolated_duration=part * preprolated_duration)
                        if factors:
                            for _ in range(part):
                                child = rhythmtreetools.RhythmTreeContainer(
                                    preprolated_duration=preprolated_duration)
                                grouping.append(child)
                                recurse(
                                    child,
                                    factors,
                                    denominator,
                                    decrease_durations_monotonically,
                                    )
                        else:
                            for _ in range(part):
                                grouping.append(
                                    rhythmtreetools.RhythmTreeLeaf(
                                        preprolated_duration=(1, denominator)))
                        node.append(grouping)
            else:
                node.extend([rhythmtreetools.RhythmTreeLeaf(
                    preprolated_duration=(1, denominator))
                    for _ in range(node.preprolated_duration.numerator)])

        decrease_durations_monotonically = \
            bool(decrease_durations_monotonically)

        if isinstance(arg, type(self)):
            root = arg.root_node
            numerator, denominator = arg.numerator, arg.denominator
            decrease_durations_monotonically = \
                arg.decrease_durations_monotonically

        elif isinstance(arg, (str, rhythmtreetools.RhythmTreeContainer)):
            if isinstance(arg, str):
                parsed = rhythmtreetools.RhythmTreeParser()(arg)
                assert len(parsed) == 1
                root = parsed[0]
            else:
                root = arg
            for node in root.nodes:
                assert node.prolation == 1
            numerator = root.preprolated_duration.numerator
            denominator = root.preprolated_duration.denominator

        elif isinstance(arg, (tuple, scoretools.Measure)) or \
            (hasattr(arg, 'numerator') and hasattr(arg, 'denominator')):
            if isinstance(arg, tuple):
                fraction = mathtools.NonreducedFraction(arg)
            elif isinstance(arg, scoretools.Measure):
                time_signature = arg._get_effective_context_mark(
                    marktools.TimeSignatureMark)
                fraction = mathtools.NonreducedFraction(
                    time_signature.numerator, time_signature.denominator)
            else:
                fraction = mathtools.NonreducedFraction(
                    arg.numerator, arg.denominator)
            numerator, denominator = fraction.numerator, fraction.denominator
            factors = mathtools.factors(numerator)[1:]
            # group two nested levels of 2s into a 4
            if 1 < len(factors) and factors[0] == factors[1] == 2:
                factors[0:2] = [4]
            root = rhythmtreetools.RhythmTreeContainer(
                preprolated_duration=fraction)
            recurse(
                root,
                factors,
                denominator,
                decrease_durations_monotonically,
                )

        else:
            message = "Can't initialize {} from {!r}."
            raise ValueError(message.format(type(self).__name__, arg))

        self._root_node = root
        self._numerator = numerator
        self._denominator = denominator
        self._decrease_durations_monotonically = \
            decrease_durations_monotonically

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) == type(expr):
            if self.rtm_format == expr.rtm_format:
                return True
        return False

    def __iter__(self):
        r'''Iterate meter:

        ::

            >>> meter = \
            ...     timesignaturetools.Meter((5, 4))

        ::

            >>> for x in meter:
            ...    x
            ...
            (NonreducedFraction(0, 4), NonreducedFraction(1, 4))
            (NonreducedFraction(1, 4), NonreducedFraction(2, 4))
            (NonreducedFraction(2, 4), NonreducedFraction(3, 4))
            (NonreducedFraction(0, 4), NonreducedFraction(3, 4))
            (NonreducedFraction(3, 4), NonreducedFraction(4, 4))
            (NonreducedFraction(4, 4), NonreducedFraction(5, 4))
            (NonreducedFraction(3, 4), NonreducedFraction(5, 4))
            (NonreducedFraction(0, 4), NonreducedFraction(5, 4))

        Yield pairs.
        '''
        def recurse(node):
            result = []
            for child in node:
                if isinstance(child, rhythmtreetools.RhythmTreeLeaf):
                    result.append(child)
                else:
                    result.extend(recurse(child))
            result.append(node)
            return result
        result = recurse(self.root_node)
        for x in result:
            start_offset = mathtools.NonreducedFraction(x.start_offset
                ).with_denominator(self.denominator)
            stop_offset = mathtools.NonreducedFraction(x.stop_offset
                ).with_denominator(self.denominator)
            yield start_offset, stop_offset

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.rtm_format)

    ### PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _positional_argument_values(self):
        return (self.rtm_format,)

    ### PUBLIC PROPERTIES ###

    @property
    def decrease_durations_monotonically(self):
        r'''True if the meter divides large primes into 
        collections of ``2`` and ``3`` that decrease monotonically.
        
        ..  container:: example

            **Example 1.** Metrical hiearchy with durations that increase 
            monotonically:

            ::

                >>> meter = \
                ...     timesignaturetools.Meter((5, 4),
                ...     decrease_durations_monotonically=False)

            ::

                >>> meter.decrease_durations_monotonically
                False

            ::

                >>> print meter.pretty_rtm_format
                (5/4 (
                    (2/4 (
                        1/4
                        1/4))
                    (3/4 (
                        1/4
                        1/4
                        1/4))))

        ..  container:: example

            **Example 2.** Meter with durations that 
            decrease monotonically:

            ::

                >>> meter = \
                ...     timesignaturetools.Meter((5, 4),
                ...     decrease_durations_monotonically=True)

            ::

                >>> meter.decrease_durations_monotonically
                True

            ::

                >>> print meter.pretty_rtm_format
                (5/4 (
                    (3/4 (
                        1/4
                        1/4
                        1/4))
                    (2/4 (
                        1/4
                        1/4))))

        Returns boolean.
        '''
        return self._decrease_durations_monotonically

    @property
    def denominator(self):
        r'''Beat hierarchy denominator:

        ::

            >>> meter.denominator
            4

        Returns positive integer.
        '''
        return self._denominator

    @property
    def depthwise_offset_inventory(self):
        r'''Depthwise inventory of offsets at each grouping level:

        ::

            >>> for depth, offsets in enumerate(
            ...     meter.depthwise_offset_inventory):
            ...     print depth, offsets
            0 (Offset(0, 1), Offset(5, 4))
            1 (Offset(0, 1), Offset(3, 4), Offset(5, 4))
            2 (Offset(0, 1), Offset(1, 4), Offset(1, 2), Offset(3, 4), Offset(1, 1), Offset(5, 4))

        Returns dictionary.
        '''
        inventory = []
        for depth, nodes in sorted(
            self.root_node.depthwise_inventory.items()):
            offsets = []
            for node in nodes:
                offsets.append(durationtools.Offset(node.start_offset))
            offsets.append(
                durationtools.Offset(self.numerator, self.denominator))
            inventory.append(tuple(offsets))
        return tuple(inventory)

    @property
    def graphviz_format(self):
        r'''Graphviz format of hierarchy's root node:

        ::

            >>> print meter.graphviz_format
            digraph G {
                node_0 [label="5/4",
                    shape=triangle];
                node_1 [label="3/4",
                    shape=triangle];
                node_2 [label="1/4",
                    shape=box];
                node_3 [label="1/4",
                    shape=box];
                node_4 [label="1/4",
                    shape=box];
                node_5 [label="2/4",
                    shape=triangle];
                node_6 [label="1/4",
                    shape=box];
                node_7 [label="1/4",
                    shape=box];
                node_0 -> node_1;
                node_0 -> node_5;
                node_1 -> node_2;
                node_1 -> node_3;
                node_1 -> node_4;
                node_5 -> node_6;
                node_5 -> node_7;
            }

        ::

            >>> functiontools.graph(meter) # doctest: +SKIP

        Returns string.
        '''
        return self.root_node.graphviz_format

    @property
    def implied_time_signature(self):
        r'''Implied time signature:

        ::

            >>> timesignaturetools.Meter((4, 4)).implied_time_signature
            TimeSignatureMark((4, 4))

        Returns TimeSignatureMark object.
        '''
        return marktools.TimeSignatureMark(
            self.root_node.preprolated_duration)

    @property
    def numerator(self):
        r'''Beat hierarchy numerator:

        ::

            >>> meter.numerator
            5

        Returns positive integer.
        '''
        return self._numerator

    @property
    def preprolated_duration(self):
        r'''Beat hierarchy preprolated_duration:

        ::

            >>> meter.preprolated_duration
            Duration(5, 4)

        Returns preprolated_duration.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

    @property
    def pretty_rtm_format(self):
        r'''Beat hiearchy pretty RTM format:

        ::

            >>> print meter.pretty_rtm_format
            (5/4 (
                (3/4 (
                    1/4
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))))

        Returns string.
        '''
        return self.root_node.pretty_rtm_format

    @property
    def root_node(self):
        r'''Beat hiearchy root node:

        ::

            >>> meter.root_node
            RhythmTreeContainer(
                children=(
                    RhythmTreeContainer(
                        children=(
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                ),
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                ),
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                )
                            ),
                        preprolated_duration=NonreducedFraction(3, 4)
                        ),
                    RhythmTreeContainer(
                        children=(
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                ),
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                )
                            ),
                        preprolated_duration=NonreducedFraction(2, 4)
                        )
                    ),
                preprolated_duration=NonreducedFraction(5, 4)
                )

        Returns rhythm tree node.
        '''
        return self._root_node

    @property
    def rtm_format(self):
        r'''Beat hierarchy RTM format:

        ::

            >>> meter.rtm_format
            '(5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))'

        Returns string.
        '''
        return self._root_node.rtm_format

    @property
    def storage_format(self):
        r'''Beat hierarchy storage format:

        ::

            >>> print meter.storage_format
            timesignaturetools.Meter(
                '(5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))'
                )

        Returns string.
        '''
        return self._tools_package_qualified_indented_repr

    ### PRIVATE METHODS ###

    def _get_recurser(self):
        return recurse

    @staticmethod
    def _make_gridded_test_rhythm(grid_length, rhythm_number, denominator=16):
        r'''Make test rhythm number `rhythm_number` that fits `grid_length`.

        Returns selection of one or more possibly tied notes.

        ..  container:: example

            **Example 1.** The eight test rhythms that fit a length-``4`` 
            grid:

            ::

                >>> from abjad.tools.timesignaturetools import Meter
                >>> for rhythm_number in range(8):
                ...     notes = Meter._make_gridded_test_rhythm(
                ...         4, rhythm_number, denominator=4)
                ...     measure = Measure((4, 4), notes)
                ...     print '{}\t{}'.format(rhythm_number, str(measure))
                ...
                0   |4/4 c'1|
                1   |4/4 c'2. c'4|
                2   |4/4 c'2 c'4 c'4|
                3   |4/4 c'2 c'2|
                4   |4/4 c'4 c'4 c'2|
                5   |4/4 c'4 c'4 c'4 c'4|
                6   |4/4 c'4 c'2 c'4|
                7   |4/4 c'4 c'2.|

        ..  container:: example

            **Example 2.** The sixteenth test rhythms for that a length-``5`` 
            grid:

            ::

                >>> for rhythm_number in range(16):
                ...     notes = Meter._make_gridded_test_rhythm(
                ...         5, rhythm_number, denominator=4)
                ...     measure = Measure((5, 4), notes)
                ...     print '{}\t{}'.format(rhythm_number, str(measure))
                ...
                0   |5/4 c'1 ~ c'4|
                1   |5/4 c'1 c'4|
                2   |5/4 c'2. c'4 c'4|
                3   |5/4 c'2. c'2|
                4   |5/4 c'2 c'4 c'2|
                5   |5/4 c'2 c'4 c'4 c'4|
                6   |5/4 c'2 c'2 c'4|
                7   |5/4 c'2 c'2.|
                8   |5/4 c'4 c'4 c'2.|
                9   |5/4 c'4 c'4 c'2 c'4|
                10  |5/4 c'4 c'4 c'4 c'4 c'4|
                11  |5/4 c'4 c'4 c'4 c'2|
                12  |5/4 c'4 c'2 c'2|
                13  |5/4 c'4 c'2 c'4 c'4|
                14  |5/4 c'4 c'2. c'4|
                15  |5/4 c'4 c'1|

        Use for testing meter establishment.
        '''
        from abjad.tools import scoretools

        # check input
        assert mathtools.is_positive_integer(grid_length)
        assert isinstance(rhythm_number, int)
        assert mathtools.is_positive_integer_power_of_two(denominator)

        # find count of all rhythms that fit grid length
        rhythm_count = 2 ** (grid_length - 1)

        # read rhythm number cyclically to allow large and 
        # negative rhythm numbers
        rhythm_number = rhythm_number % rhythm_count

        # find binary representation of rhythm
        binary_representation = \
            mathtools.integer_to_binary_string(rhythm_number)
        binary_representation = binary_representation.zfill(grid_length)

        # partition binary representation of rhythm
        parts = sequencetools.partition_sequence_by_value_of_elements(
            binary_representation)

        # find durations
        durations = [
            durationtools.Duration(len(part), denominator) 
            for part in parts
            ]

        # make notes
        notes = scoretools.make_notes([0], durations)

        # return notes
        return notes

    ### PUBLIC METHODS ###

    def generate_offset_kernel_to_denominator(
        self, denominator, normalize=True):
        r'''Generate a dictionary of all offsets in a meter up
        to `denominator`, where the keys are the offsets and the values
        are the normalized weights of those offsets:

        ::

            >>> meter = \
            ...     timesignaturetools.Meter((4, 4))
            >>> kernel = \
            ...     meter.generate_offset_kernel_to_denominator(8)
            >>> for offset, weight in sorted(kernel.kernel.iteritems()):
            ...     print '{}\t{}'.format(offset, weight)
            ...
            0       3/16
            1/8     1/16
            1/4     1/8
            3/8     1/16
            1/2     1/8
            5/8     1/16
            3/4     1/8
            7/8     1/16
            1       3/16

        This is useful for testing how strongly a collection of offsets
        responds to a given meter.

        Returns dictionary.
        '''
        from abjad.tools import timesignaturetools
        assert mathtools.is_positive_integer_power_of_two(
            denominator / self.denominator)

        inventory = list(self.depthwise_offset_inventory)
        old_flag_count = durationtools.Duration(1, self.denominator).flag_count
        new_flag_count = durationtools.Duration(1, denominator).flag_count
        extra_depth = new_flag_count - old_flag_count
        for _ in range(extra_depth):
            old_offsets = inventory[-1]
            new_offsets = []
            for first, second in \
                sequencetools.iterate_sequence_pairwise_strict(old_offsets):
                new_offsets.append(first)
                new_offsets.append((first + second) / 2)
            new_offsets.append(old_offsets[-1])
            inventory.append(tuple(new_offsets))

        total = 0
        kernel = {}
        for offsets in inventory:
            for offset in offsets:
                if offset not in kernel:
                    kernel[offset] = 0
                kernel[offset] += 1
                total += 1

        if normalize:
            for offset, response in kernel.iteritems():
                kernel[offset] = durationtools.Multiplier(response, total)

        return timesignaturetools.MetricAccentKernel(kernel)