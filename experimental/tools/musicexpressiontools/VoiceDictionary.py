# -*- encoding: utf-8 -*-
import collections
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate
from abjad.tools.abctools.AbjadObject import AbjadObject


class VoiceDictionary(AbjadObject, collections.OrderedDict):
    r'''Voice dictionary.
    '''

    ### INITIALIZER ###

    def __init__(self, score):
        assert isinstance(score, scoretools.Score), repr(score)
        collections.OrderedDict.__init__(self)
        self._score = score
        self._initialize_voice_proxies()

    ### SPECIAL METHODS ###

    def __repr__(self):
        contents = ', '.join([repr(x) for x in self])
        return '{}([{}])'.format(type(self).__name__, contents)

    def __setitem__(self, key, value):
        from experimental.tools import musicexpressiontools
        assert isinstance(key, str), repr(key)
        assert isinstance(value, musicexpressiontools.VoiceProxy), repr(value)
        collections.OrderedDict.__setitem__(self, key, value)

    ### PRIVATE METHODS ###

    def _initialize_voice_proxies(self):
        from experimental.tools import musicexpressiontools
        voice_names = []
        if self.score is not None:
            for voice in iterate(self.score).by_class(scoretools.Voice):
                assert voice.context_name is not None, voice.name_name
                voice_names.append(voice.name)
        for voice_name in sorted(voice_names):
            self[voice_name] = musicexpressiontools.VoiceProxy()

    ### PUBLIC PROPERTIES ###

    @property
    def score(self):
        r'''Voice dictionary score.

        Returns score.
        '''
        return self._score
