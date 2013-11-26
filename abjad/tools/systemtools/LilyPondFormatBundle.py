# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LilyPondFormatBundle(AbjadObject):
    r'''LilyPond format bundle.

    Transient class created to hold the collection of all
    format contributions generated on behalf of a single component.
    '''

    ### CLASS VARIABLES ###

    __slots__ =  (
        '_before',
        '_after',
        '_opening',
        '_closing',
        '_right',
        '_context_settings',
        '_grob_overrides',
        '_grob_reverts',
        )

    ### INNER CLASS DEFINITION ###

    class SlotContributions(object):
        
        __slots__ = (
            '_articulations',
            '_commands',
            '_comments',
            '_indicators',
            '_markup',
            '_spanners',
            '_stem_tremolos',
            )

        def __init__(self):
            self._articulations = []
            self._commands = []
            self._comments = []
            self._indicators = []
            self._markup = []
            self._spanners = []
            self._stem_tremolos = []

        @property
        def articulations(self):
            return self._articulations

        @property
        def comments(self):
            return self._comments

        @property
        def commands(self):
            return self._commands

        @property
        def indicators(self):
            return self._indicators

        @property
        def markup(self):
            return self._markup

        @property
        def spanners(self):
            return self._spanners

        @property
        def stem_tremolos(self):
            return self._stem_tremolos

        def alphabetize(self):
            self._indicators.sort()

        def get(self, identifier):
            return getattr(self, identifier) 

        def make_immutable(self):
            self._articulations = tuple(sorted(self.articulations))
            self._commands = tuple(self.commands)
            self._comments = tuple(self.comments)
            self._indicators = tuple(self.indicators)
            self._markup = tuple(self.markup)
            self._spanners = tuple(self.spanners)
            self._stem_tremolos = tuple(self.stem_tremolos)
    
    ### INITIALIZER ###

    def __init__(self):
        self._before = self.SlotContributions()
        self._after = self.SlotContributions()
        self._opening = self.SlotContributions()
        self._closing = self.SlotContributions()
        self._right = self.SlotContributions()
        self._context_settings = []
        self._grob_overrides = []
        self._grob_reverts = []

    ### PUBLIC PROPERTIES ###

    @property
    def after(self):
        return self._after

    @property
    def before(self):
        return self._before

    @property
    def closing(self):
        return self._closing

    @property
    def context_settings(self):
        return self._context_settings

    @property
    def grob_overrides(self):
        return self._grob_overrides

    @property
    def grob_reverts(self):
        return self._grob_reverts

    @property
    def opening(self):
        return self._opening

    @property
    def right(self):
        return self._right

    ### PUBLIC METHODS ###

    def alphabetize(self):
        self.before.alphabetize()
        self.after.alphabetize()
        self.opening.alphabetize()
        self.closing.alphabetize()
        self.right.alphabetize()
        self._context_settings.sort()
        self._grob_overrides.sort()
        self._grob_reverts.sort()
        
    def get(self, identifier):
        return getattr(self, identifier)

    def make_immutable(self):
        self.before.make_immutable()
        self.after.make_immutable()
        self.opening.make_immutable()
        self.closing.make_immutable()
        self.right.make_immutable()
        self._context_settings = tuple(self.context_settings)
        self._grob_overrides = tuple(self.grob_overrides)
        self._grob_reverts = tuple(self.grob_reverts)
