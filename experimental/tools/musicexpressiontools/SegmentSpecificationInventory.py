# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class SegmentSpecificationInventory(AbjadObject, list):
    r'''Segment specification inventory.
    '''

    ### INITIALIZER ###

    def __init__(self, *args):
        list.__init__(self, *args)

    ### SPECIAL METHODS ###

    def __getitem__(self, arg):
        if isinstance(arg, int):
            return list.__getitem__(self, arg)
        elif isinstance(arg, str):
            for segment in self:
                if segment.segment_name == arg:
                    return segment
            else:
                raise KeyError(repr(arg))

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, list.__repr__(self))
