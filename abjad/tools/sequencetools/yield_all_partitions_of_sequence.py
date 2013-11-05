# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def yield_all_partitions_of_sequence(sequence):
    '''Yield all partitions of `sequence`:

    ::

        >>> for partition in sequencetools.yield_all_partitions_of_sequence([0, 1, 2, 3]):
        ...     partition
        ...
        [[0, 1, 2, 3]]
        [[0, 1, 2], [3]]
        [[0, 1], [2, 3]]
        [[0, 1], [2], [3]]
        [[0], [1, 2, 3]]
        [[0], [1, 2], [3]]
        [[0], [1], [2, 3]]
        [[0], [1], [2], [3]]

    Returns generator of newly created lists.
    '''

    # TODO: remove type restriction #
    if not isinstance(sequence, list):
        raise TypeError('%s must be list.' % sequence)

    partitions = []

    len_l_minus_1 = len(sequence) - 1
    for i in range(2 ** len_l_minus_1):
        binary_string = mathtools.integer_to_binary_string(i)
        binary_string = binary_string.zfill(len_l_minus_1)
        part = sequence[0:1]
        partition = [part]
        for n, indicator in zip(sequence[1:], binary_string):
            if int(indicator) == 0:
                part.append(n)
            else:
                part = [n]
                partition.append(part)
        partitions.append(partition)

    return partitions