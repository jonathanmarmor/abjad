from abjad.tools import introspectiontools
from experimental.specificationtools.Selector import Selector


class BackgroundElementSelector(Selector):
    r'''.. versionadded:: 1.0

    Select one background object with mandatory `klass` and `index`.

    Select segment ``'red'``::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.BackgroundElementSelector(specificationtools.Segment, 'red')
        BackgroundElementSelector(specificationtools.Segment, 'red')

    Select segment ``0``::

        >>> specificationtools.BackgroundElementSelector(specificationtools.Segment, 0)
        BackgroundElementSelector(specificationtools.Segment, 0)

    Select measure ``0``::

        >>> specificationtools.BackgroundElementSelector(measuretools.Measure, 0)
        BackgroundElementSelector(measuretools.Measure, 0)

    Select division ``0``::

        >>> specificationtools.BackgroundElementSelector(specificationtools.Division, 0)
        BackgroundElementSelector(specificationtools.Division, 0)

    More examples to follow.
    '''

    ### INITIALIZER ###
    
    def __init__(self, klass, index):
        from experimental import specificationtools
        assert specificationtools.is_background_element_klass(klass), repr(klass)
        assert isinstance(index, (int, str)), repr(index)
        Selector.__init__(self)
        self._klass = klass
        self._index = index

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.klass == expr.klass:
                if self.index == expr.index:
                    return True
        return False

    def __repr__(self):
        klass = introspectiontools.klass_to_tools_package_qualified_klass_name(self.klass)
        return '{}({}, {!r})'.format(self._class_name, klass, self.index)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def index(self):
        '''Background element selector index initialized by user.

        Return integer or string.
        '''
        return self._index

    @property
    def klass(self):
        '''Background element selector class initialized by user.

        Return segment, measure or division class.
        '''
        return self._klass
